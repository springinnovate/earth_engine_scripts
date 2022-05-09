"""Samples GEE assets using provided CSV point tables."""
from datetime import datetime
import argparse
import functools
import os
import json
import logging
import math

from ecoshard import taskgraph
import geopandas
import ee
import numpy
import pandas


logging.basicConfig(
    level=logging.DEBUG,
    format=(
        '%(asctime)s (%(relativeCreated)d) %(levelname)s %(name)s'
        ' [%(funcName)s:%(lineno)d] %(message)s'))
logging.getLogger('fiona').setLevel(logging.WARN)
logging.getLogger('ecoshard.taskgraph').setLevel(logging.WARN)
LOGGER = logging.getLogger(__name__)


MODIS_ID = 'MODIS'
NLCD_ID = 'NLCD'
CORINE_ID = 'CORINE'

POLY_IN_FIELD = 'POLY-in'
POLY_OUT_FIELD = 'POLY-out'
PREV_YEAR_TAG = '-prev-year'

RASTER_DB = {
    NLCD_ID: {
        'asset_id': 'USGS/NLCD_RELEASES/2016_REL',
        'valid_years': numpy.array([
            1992, 2001, 2004, 2006, 2008, 2011, 2013, 2016]),
        'closest_year_field': 'NLCD-year',
        'natural_field': 'NLCD-natural',
        'cultivated_field': 'NLCD-cultivated',
        'natural_id_list': [(41, 74), (90, 95)],
        'cultivated_id_list': [(81, 82)],
        },
    CORINE_ID: {
        'asset_id': 'COPERNICUS/CORINE/V20/100m',
        'valid_years': numpy.array([1990, 2000, 2006, 2012, 2018]),
        'closest_year_field': 'CORINE-year',
        'natural_field': 'CORINE-natural',
        'cultivated_field': 'CORINE-cultivated',
        'natural_id_list': [(311, 423)],
        'cultivated_id_list': [(211, 244)],
    },
    MODIS_ID: {
        'asset_id': 'MODIS/006/MCD12Q2',
        'valid_years': numpy.array(range(2001, 2010)),
        'julian_day_variables': [
            'Greenup_1',
            'MidGreenup_1',
            'Peak_1',
            'Maturity_1',
            'MidGreendown_1',
            'Senescence_1',
            'Dormancy_1',
            ],
        'raw_variables': [
            'EVI_Minimum_1',
            'EVI_Amplitude_1',
            'EVI_Area_1',
            'QA_Overall_1',
            ]
    },
}

REDUCER = 'mean'


def _filter_and_buffer_points_by_year(
        point_table, lat_field, long_field, year_field, point_buffer):
    """Separate points in Geopandas table by year.

    Args:
        point_table (geopandas.Dataframe): table with lat/lng and year fields
        lat_field (str): fieldname for lat in ``table``
        long_field (str): fieldname for long in ``table``
        year_field (str): fieldname for year in ``table``
        point_buffer (float): distance in m to buffer points

    Returns:
        dict of list of ee.Features of points indexed by year from ``table``
    """
    pts_by_year = {}
    for year in point_table[year_field].unique():
        pts_by_year[year] = ee.FeatureCollection([
            ee.Feature(ee.Geometry.Point(
                row[long_field], row[lat_field]).buffer(point_buffer),
                row.to_dict())
            for index, row in point_table[
                point_table[year_field] == year].dropna().iterrows()])
    return pts_by_year


def _load_ee_poly(polygon_path):
    """Read a polygon path from disk and convert to WGS84 GEE Polygon."""
    gp_poly = geopandas.read_file(polygon_path).to_crs('EPSG:4326')
    json_poly = json.loads(gp_poly.to_json())
    coords = [
        json_feature['geometry']['coordinates']
        for json_feature in json_poly['features']]
    ee_poly = ee.Geometry.MultiPolygon(coords)
    return ee_poly


def _get_closest_num(number_list, candidate):
    """Return closest number in sorted list."""
    index = (numpy.abs(number_list - candidate)).argmin()
    return int(number_list[index])


def _calculate_natural_cultivated_masks(dataset_id, year):
    """Create a natural/cultivated mask given a dataset and list of valid ids.

    Args:
        dataset_id (str): a string representing a valid entry in
            ``RASTER_DB`` that contains indexes for
            'valid_years', 'cultivated_id_list', 'cultivated_field',
            'natural_field', 'natural_id_list'.
        year (int): a year to sample from the given dataset

    Return:
        natural_mask (ee.Image == 1 where natural),
        cultivated_mask (ee.Image == 1 where cultivated),
        closest_year (int indicating closest year match to requested)
    """
    raster = RASTER_DB[dataset_id]
    closest_year = _get_closest_num(raster['valid_years'], year)
    image_collection = ee.ImageCollection(raster['asset_id'])

    landcover_image = image_collection.filter(
        ee.Filter.eq('system:index', str(closest_year))).first().select(
        'landcover')

    mask_dict = {
        'natural_mask': ee.Image(0),
        'cultivated_mask': ee.Image(0)
    }
    for mask_id, id_list, band_name in [
            ('cultivated_mask',
             raster['cultivated_id_list'], raster['cultivated_field']),
            ('natural_mask',
             raster['natural_id_list'], raster['natural_field'])]:
        for (low_id, high_id) in id_list:
            mask_dict[mask_id] = mask_dict[mask_id].Or(
                landcover_image.gte(low_id).And(landcover_image.lte(high_id)))
        mask_dict[mask_id] = mask_dict[mask_id].rename(band_name)

    return (
        mask_dict['natural_mask'],
        mask_dict['cultivated_mask'],
        closest_year)


def _sample_modis_by_year(pts_by_year, cult_nat_raster_id_list, ee_poly, sample_scale):
    """Sample MODIS variables by year with NLCD/CORINE/polygon intersection.

    Sample all variables from https://docs.google.com/spreadsheets/d/1nbmCKwIG29PF6Un3vN6mQGgFSWG_vhB6eky7wVqVwPo

    Args:
        pts_by_year (dict): dictionary of list of points indexed by year.
        cult_nat_raster_id_list (list): list of entries in RASTER_DB that are used
            for cultivated and natural masking to additionally mask
            MODIS products
        ee_poly (ee.Polygon): if not None, additionally filter samples by
            in/out of polygon.
        sample_scale (float): scale to sample rasters in meters

    Returns:
        set of all property ids generated by this call,
        list of dict for each point with values for given properties

    """
    modis_db = RASTER_DB[MODIS_ID]
    # this is the year that julian times are based on for MODIS
    epoch_date = datetime.strptime('1970-01-01', "%Y-%m-%d")
    modis_phen = ee.ImageCollection(modis_db['asset_id'])

    # this is the result that is returned -- points with sampled features
    point_sample_list = []

    band_id_set = set()

    if ee_poly:
        poly_mask = ee.Image(0).clip(ee_poly).add(1).unmask()
        inv_polymask = poly_mask.Not()

    for year in pts_by_year.keys():
        LOGGER.info(f'processing year {year}')

        LOGGER.info('process MODIS')
        band_list = []
        for active_year, band_name_suffix in (
                (year, ''), (year-1, PREV_YEAR_TAG)):
            # active year is stored as a string
            if int(active_year) in modis_db['valid_years']:
                LOGGER.info(
                    f'modis active_year: {active_year}/{band_name_suffix}')

                for cult_nat_raster_id in [''] + cult_nat_raster_id_list:
                    if cult_nat_raster_id:
                        natural_mask, cultivated_mask, closest_year = (
                            _calculate_natural_cultivated_masks(
                                cult_nat_raster_id, active_year))
                        LOGGER.debug(closest_year)
                        closest_year_id = f'{cult_nat_raster_id}-closest-year{band_name_suffix}'
                        band_id_set.add(closest_year_id)
                        band_list.append(ee.Image(
                            int(closest_year)).rename(closest_year_id))
                        mask_loop_args = [
                            (natural_mask, f'-{cult_nat_raster_id}-natural{band_name_suffix}'),
                            (cultivated_mask, f'-{cult_nat_raster_id}-cultivated{band_name_suffix}')]

                        for mask_raster, band_suffix in mask_loop_args:
                            cult_ag_band_id = f'{band_suffix[1:]}'
                            band_id_set.add(cult_ag_band_id)
                            band_list.append(
                                mask_raster.rename(cult_ag_band_id))
                    else:
                        mask_loop_args = [(ee.Image(1), band_name_suffix)]

                    for mask_raster, band_suffix in mask_loop_args:
                        # Get date based values and convert to be days since start
                        # of active_year
                        modis_band_renames = [
                            f'{MODIS_ID}-{field}{band_suffix}'
                            for field in modis_db['julian_day_variables']]
                        band_id_set = band_id_set.union(set(modis_band_renames))
                        bands_since_1970 = modis_phen.select(
                            modis_db['julian_day_variables']).filterDate(
                            f'{active_year}-01-01', f'{active_year}-12-31')

                        current_year = datetime.strptime(
                            f'{active_year}-01-01', "%Y-%m-%d")
                        days_since_epoch = (current_year - epoch_date).days
                        julian_day_bands = (
                            bands_since_1970.toBands()).subtract(days_since_epoch).updateMask(mask_raster)
                        band_list.append(
                            julian_day_bands.rename(modis_band_renames))

                        raw_variable_bands = modis_phen.select(
                            modis_db['raw_variables']).filterDate(
                            f'{active_year}-01-01', f'{active_year}-12-31').toBands().updateMask(mask_raster)
                        raw_band_renames = [
                            f'{MODIS_ID}-{field}{band_suffix}'
                            for field in modis_db['raw_variables']]
                        band_id_set = band_id_set.union(set(raw_band_renames))
                        band_list.append(raw_variable_bands.rename(raw_band_renames))

        LOGGER.info(f'summarize by points for year {year}')
        year_points = pts_by_year[year]
        # determine area in/out of point area
        if ee_poly:
            LOGGER.info('calculate area in/out of polygon per point')

            def area_in_out(feature):
                """Calculate area inside/outside of poly for given feature."""
                feature_area = feature.area()
                area_in = ee_poly.intersection(feature.geometry()).area()
                return feature.set({
                    POLY_OUT_FIELD: (
                        feature_area.subtract(area_in)).divide(feature_area),
                    POLY_IN_FIELD: area_in.divide(feature_area)})
            year_points = year_points.map(area_in_out)
            band_id_set = band_id_set.union(
                set([POLY_OUT_FIELD, POLY_IN_FIELD]))

            for band in list(band_list):
                band_name_list = band.bandNames().getInfo()
                poly_in_band_names = [
                    f'{name}-{POLY_IN_FIELD}' for name in band_name_list]
                poly_out_band_names = [
                    f'{name}-{POLY_OUT_FIELD}' for name in band_name_list]
                band_id_set = band_id_set.union(
                    set(poly_in_band_names+poly_out_band_names))

                band_list.append(band.multiply(poly_mask).rename(
                    poly_in_band_names))

                band_list.append(band.multiply(inv_polymask).rename(
                    poly_out_band_names))

                # if export_flag:
                #     LOGGER.info('************** exporting asset')
                #     task = ee.batch.Export.image.toAsset(**{
                #         'image': poly_mask,
                #         'description': 'poly_mask6',
                #         'assetId': 'users/richsharp/poly_mask6',
                #         'scale': 500,
                #         'region': ee_poly,
                #         'crs': 'EPSG:4326', })
                #     task.start()
                #     task = ee.batch.Export.image.toAsset(**{
                #         'image': inv_polymask,
                #         'description': 'inv_polymask6',
                #         'assetId': 'users/richsharp/inv_polymask6',
                #         'scale': 500,
                #         'region': ee_poly,
                #         'crs': 'EPSG:4326', })
                #     task.start()
                #     export_flag = False
                #     LOGGER.debug(task)

        all_bands = functools.reduce(lambda x, y: x.addBands(y), band_list)

        year_point_samples = all_bands.reduceRegions(**{
            'collection': year_points,
            'reducer': REDUCER,
            'scale': sample_scale,
            })
        point_sample_list.extend([
            x['properties'] for x in year_point_samples.getInfo()['features']])

        LOGGER.info('************** exporting asset')
        task = ee.batch.Export.image.toAsset(**{
         'image': all_bands,
         'description': 'allbands',
         'assetId': 'users/richsharp/allbands',
         'scale': 500,
         'region': ee_poly,
         'crs': 'EPSG:4326', })
        task.start()
        LOGGER.debug(task)

    return band_id_set, point_sample_list


def main():
    """Entry point."""
    parser = argparse.ArgumentParser(
        description='Sample MODIS biophyisical areas on point data with additional information specified about cultivated/natural areas.')
    parser.add_argument('csv_path', help='path to CSV data table')
    parser.add_argument('--year_field', default='crop_year', help='field name in csv_path for year, default `year_field`')
    parser.add_argument('--long_field', default='field_longitude', help='field name in csv_path for longitude, default `long_field`')
    parser.add_argument('--lat_field', default='field_latitude', help='field name in csv_path for latitude, default `lat_field')
    parser.add_argument('--point_buffer', type=float, default=1000, help='buffer distance in meters around point to do aggregate analysis, default 1000m')
    parser.add_argument('--nlcd', default=False, action='store_true', help='sample the NCLD landcover for cultivated/natural masks')
    parser.add_argument('--corine', default=False, action='store_true', help='sample the CORINE landcover for cultivated/natural masks')
    parser.add_argument('--polygon_path', type=str, help='this polygon modifies samples to include inside and outside of the sampled datasets')
    parser.add_argument('--n_rows', type=int, help='limit the number of points read from the CSV to this value, useful for debugging.')
    parser.add_argument('--sample_scale', type=float, default=500.0, help='scale to sample rasters in meters, defaults to 500m')
    parser.add_argument('--batch_size', type=int, default=100, help='point batch size to limit processing on GEE, defaults to 100')
    parser.add_argument('--authenticate', action='store_true', help='Pass this flag if you need to reauthenticate with GEE')
    args = parser.parse_args()

    landcover_options = [x for x in ['nlcd', 'corine'] if vars(args)[x]]
    landcover_substring = '_'.join(landcover_options)
    if args.authenticate:
        ee.Authenticate()
    ee.Initialize()
    point_table = pandas.read_csv(
        args.csv_path, converters={
            args.long_field: lambda x: float(x),
            args.lat_field: lambda x: float(x),
            args.year_field: lambda x: int(x),
        },
        nrows=args.n_rows)

    LOGGER.info(f'break out points by year and buffer to {args.point_buffer}m')
    sample_keys = set()
    sample_list = []

    task_graph = taskgraph.TaskGraph('.', -1)

    cult_nat_raster_id_list = []
    if args.nlcd:
        cult_nat_raster_id_list.append(NLCD_ID)
    if args.corine:
        cult_nat_raster_id_list.append(CORINE_ID)

    for index in range(math.ceil(point_table.shape[0]/args.batch_size)):
        min_index = index*args.batch_size
        max_index = (index+1)*args.batch_size
        sample_task = task_graph.add_task(
            func=_sample_table,
            args=(
                point_table, min_index, max_index, args.lat_field,
                args.long_field, args.year_field, args.point_buffer,
                cult_nat_raster_id_list, args.polygon_path, args.sample_scale),
            store_result=True,
            task_name=f'sample table on index {index}')

        local_sample_keys, local_sample_list = sample_task.get()
        sample_keys = sample_keys.union(local_sample_keys)
        sample_list.extend(local_sample_list)

    # take out the point table columns so we can do them first
    sample_keys = list(sorted(sample_keys))
    table_keys = point_table.columns

    poly_str = '_'
    if args.polygon_path:
        poly_str += 'poly_'

    table_path = f'sampled_{args.point_buffer}m_{landcover_substring}{poly_str}{os.path.basename(args.csv_path)}'
    with open(table_path, 'w') as table_file:
        table_file.write(
            ','.join(table_keys) + f',{",".join(sample_keys)}\n')
        for sample in sample_list:
            table_file.write(
                ','.join([str(sample[key]) for key in table_keys]) + ',')
            table_file.write(','.join([
                'invalid' if field not in sample else
                str(sample[field]) for field in sample_keys]) + '\n')


def _sample_table(
        point_table, min_index, max_index, lat_field, long_field, year_field,
        point_buffer, cult_nat_raster_id_list, polygon_path, sample_scale):
    local_point_table = point_table[min_index:max_index]
    pts_by_year = _filter_and_buffer_points_by_year(
        local_point_table, lat_field, long_field, year_field, point_buffer)

    LOGGER.info(
        f'calculating pheno variables for {min_index}:{max_index}')

    ee_poly = None
    if polygon_path:
        ee_poly = _load_ee_poly(polygon_path)

    local_sample_keys, local_sample_list = _sample_modis_by_year(
        pts_by_year, cult_nat_raster_id_list, ee_poly, sample_scale)
    return (local_sample_keys, local_sample_list)


if __name__ == '__main__':
    main()
