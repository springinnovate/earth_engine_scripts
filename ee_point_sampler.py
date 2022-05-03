"""Samples GEE assets using provided CSV point tables."""
from datetime import datetime
import argparse
import os
import json

import geopandas
import ee
import numpy
import pandas


REDUCER = 'mean'

LANDUSE_RASTERS = {
    'nlcd': {
        'dataset': 'USGS/NLCD_RELEASES/2016_REL',
        'valid_years': numpy.array([
            1992, 2001, 2004, 2006, 2008, 2011, 2013, 2016]),
        'closest_year_field': 'NLCD-year',
        'natural_field': 'NLCD-natural',
        'cultivated_field': 'NLCD-cultivated',
        'natural_id_list': [(41, 74), (90, 95)],
        'cultivated_id_list': [(81, 82)],
        },
    'corine': {
        'dataset': 'COPERNICUS/CORINE/V20/100m',
        'valid_years': numpy.array([1990, 2000, 2006, 2012, 2018]),
        'closest_year_field': 'CORINE-year',
        'natural_field': 'CORINE-natural',
        'cultivated_field': 'CORINE-cultivated',
        'natural_id_list': [(311, 423)],
        'cultivated_id_list': [(211, 244)],
    }
}

POLY_IN_FIELD = 'POLY-in'
POLY_OUT_FIELD = 'POLY-out'

PREV_YEAR_TAG = '-prev-year'

MODIS_DATASET_NAME = 'MODIS/006/MCD12Q2'  # 500m resolution
VALID_MODIS_RANGE = (2001, 2019)


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
            ``LANDUSE_RASTERS`` that contains indexes for
            'valid_years', 'cultivated_id_list', 'cultivated_field',
            'natural_field', 'natural_id_list'.
        year (int): a year to sample from the given dataset

    Return:
        natural_mask (ee.Image == 1 where natural),
        cultivated_mask (ee.Image == 1 where cultivated),
        closest_year (int indicating closest year match to requested)
    """
    raster = LANDUSE_RASTERS[dataset_id]
    closest_year = _get_closest_num(raster['valid_years'], year)
    image_collection = ee.ImageCollection(raster['dataset'])

    landcover_image = image_collection.filter(
        ee.Filter.eq('system:index', str(closest_year))).first().select(
        'landcover')

    natural_mask = ee.Image(0)
    cultivated_mask = ee.Image(0)
    for mask_image, id_list, band_name in [
            (natural_mask,
             raster['cultivated_id_list'], raster['natural_field']),
            (cultivated_mask,
             raster['natural_id_list'], raster['cultivated_field'])]:
        for (low_id, high_id) in id_list:
            mask_image = mask_image.Or(
                landcover_image.gte(low_id).And(landcover_image.lte(high_id)))
        mask_image = mask_image.rename(band_name)

    return natural_mask, cultivated_mask, closest_year


def _nlcd_natural_cultivated_mask(year, ee_poly):
    """Natural for NLCD in 41-74 or 90-95."""
    closest_year = _get_closest_num(NLCD_VALID_YEARS, year)
    nlcd_imagecollection = ee.ImageCollection(NLCD_DATASET)
    nlcd_year = nlcd_imagecollection.filter(
        ee.Filter.eq('system:index', str(closest_year))).first().select('landcover')
    # natural 41-74 & 90-95
    natural_mask = ee.Image(0).where(
        nlcd_year.gte(41).And(nlcd_year.lte(74)).Or(
            nlcd_year.gte(90).And(nlcd_year.lte(95))), 1)
    natural_mask = natural_mask.rename(NLCD_NATURAL_FIELD)

    cultivated_mask = ee.Image(0).where(
        nlcd_year.gte(81).And(nlcd_year.lte(82)), 1)
    cultivated_mask = cultivated_mask.rename(NLCD_CULTIVATED_FIELD)

    if not ee_poly:
        return natural_mask, cultivated_mask, closest_year

    # create masks of in/out using same bounds as base image
    polymask = natural_mask.updateMask(ee.Image(1).clip(ee_poly)).unmask().gt(0)
    inv_polymask = polymask.unmask().Not()

    natural_mask_in = natural_mask.updateMask(polymask)
    cultivated_mask_in = cultivated_mask.updateMask(polymask)
    closest_year_in = closest_year.updateMask(polymask)
    natural_mask_out = natural_mask.updateMask(inv_polymask)
    cultivated_mask_out = cultivated_mask.updateMask(inv_polymask)
    closest_year_out = closest_year.updateMask(inv_polymask)

    return (
        natural_mask_in, cultivated_mask_in,
        natural_mask_out, cultivated_mask_out, closest_year)


def _sample_pheno(pts_by_year, nlcd_flag, corine_flag, ee_poly):
    """Sample phenology variables from https://docs.google.com/spreadsheets/d/1nbmCKwIG29PF6Un3vN6mQGgFSWG_vhB6eky7wVqVwPo

    Args:
        pts_by_year:
        nlcd_flag (bool): if True, sample the NLCD dataset
        corine_flag (bool): if True, sample the CORINE dataset
        ee_poly (ee.Polygon): if not None, additionally filter samples on the
            nlcd/corine datasets to see what's in or out.

    Returns:
        header_fields (list):

    """
    # these variables are measured in days since 1-1-1970
    julian_day_variables = [
        'Greenup_1',
        'MidGreenup_1',
        'Peak_1',
        'Maturity_1',
        'MidGreendown_1',
        'Senescence_1',
        'Dormancy_1',
        ]

    # these variables are direct quantities
    raw_variables = [
        'EVI_Minimum_1',
        'EVI_Amplitude_1',
        'EVI_Area_1',
        'QA_Overall_1',
        ]

    epoch_date = datetime.strptime('1970-01-01', "%Y-%m-%d")
    modis_phen = ee.ImageCollection(MODIS_DATASET_NAME)

    header_fields = [
        f'{MODIS_DATASET_NAME}-{field}'
        for field in julian_day_variables+raw_variables]

    header_fields_with_prev_year = [
        x for field in header_fields for x in (field, field+PREV_YEAR_TAG)]

    if nlcd_flag:
        header_fields_with_prev_year += [
            x for field in header_fields
            for x in (
                field+'-'+NLCD_NATURAL_FIELD,
                field+PREV_YEAR_TAG+'-'+NLCD_NATURAL_FIELD,
                field+'-'+NLCD_CULTIVATED_FIELD,
                field+PREV_YEAR_TAG+'-'+NLCD_CULTIVATED_FIELD)]

    if corine_flag:
        header_fields_with_prev_year += [
            x for field in header_fields
            for x in (
                field+'-'+CORINE_NATURAL_FIELD,
                field+PREV_YEAR_TAG+'-'+CORINE_NATURAL_FIELD,
                field+'-'+CORINE_CULTIVATED_FIELD,
                field+PREV_YEAR_TAG+'-'+CORINE_CULTIVATED_FIELD)]

    if nlcd_flag:
        if ee_poly:
            header_fields_with_prev_year.append(
                f'{NLCD_NATURAL_FIELD}-{POLY_IN_FIELD}')
            header_fields_with_prev_year.append(
                f'{NLCD_CULTIVATED_FIELD}-{POLY_IN_FIELD}')
            header_fields_with_prev_year.append(
                f'{NLCD_NATURAL_FIELD}-{POLY_OUT_FIELD}')
            header_fields_with_prev_year.append(
                f'{NLCD_CULTIVATED_FIELD}-{POLY_OUT_FIELD}')
        else:
            header_fields_with_prev_year.append(NLCD_NATURAL_FIELD)
            header_fields_with_prev_year.append(NLCD_CULTIVATED_FIELD)
        header_fields_with_prev_year.append(NLCD_CLOSEST_YEAR_FIELD)

    if corine_flag:
        header_fields_with_prev_year.append(CORINE_NATURAL_FIELD)
        header_fields_with_prev_year.append(CORINE_CULTIVATED_FIELD)
        header_fields_with_prev_year.append(CORINE_CLOSEST_YEAR_FIELD)

    if ee_poly:
        header_fields_with_prev_year.append(POLY_IN_FIELD)
        header_fields_with_prev_year.append(POLY_OUT_FIELD)

    sample_list = []
    for year in pts_by_year.keys():
        print(f'processing year {year}')
        year_points = pts_by_year[year]
        all_bands = None

        if nlcd_flag:
            if not ee_poly:
                nlcd_natural_mask, nlcd_cultivated_mask, nlcd_closest_year = \
                    _nlcd_natural_cultivated_mask(year, None)
            else:
                (nlcd_natural_mask_poly_in, nlcd_cultivated_mask_poly_in,
                 nlcd_natural_mask_poly_out, nlcd_cultivated_mask_poly_out,
                 nlcd_closest_year) = \
                    _nlcd_natural_cultivated_mask(year, ee_poly)
            print(f'nlcd_closest_year: {nlcd_closest_year}')

        if corine_flag:
            corine_natural_mask, corine_cultivated_mask, corine_closest_year = \
                _corine_natural_cultivated_mask(year)

        for active_year, band_name_suffix in (
                (year, ''), (year-1, PREV_YEAR_TAG)):
            if VALID_MODIS_RANGE[0] <= active_year <= VALID_MODIS_RANGE[1]:
                print(f'modis active_year: {active_year}')
                current_year = datetime.strptime(
                    f'{active_year}-01-01', "%Y-%m-%d")
                days_since_epoch = (current_year - epoch_date).days
                modis_band_names = [
                    x+band_name_suffix
                    for x in header_fields[0:len(julian_day_variables)]]
                bands_since_1970 = modis_phen.select(
                    julian_day_variables).filterDate(
                    f'{active_year}-01-01', f'{active_year}-12-31')
                julian_day_bands = (
                    bands_since_1970.toBands()).subtract(days_since_epoch)
                julian_day_bands = julian_day_bands.rename(modis_band_names)
                raw_band_names = [
                    x+band_name_suffix
                    for x in header_fields[len(julian_day_variables)::]]
                raw_variable_bands = modis_phen.select(
                    raw_variables).filterDate(
                    f'{active_year}-01-01', f'{active_year}-12-31').toBands()
                raw_variable_bands = raw_variable_bands.rename(raw_band_names)

                local_band_stack = julian_day_bands.addBands(raw_variable_bands)
                all_band_names = modis_band_names+raw_band_names

                if all_bands is None:
                    all_bands = local_band_stack
                else:
                    all_bands = all_bands.addBands(local_band_stack)

            # mask raw variable bands by cultivated/natural
            if nlcd_flag:
                if not ee_poly:
                    nlcd_cultivated_variable_bands = local_band_stack.updateMask(
                        nlcd_cultivated_mask)
                    nlcd_cultivated_variable_bands = \
                        nlcd_cultivated_variable_bands.rename([
                            band_name+'-'+NLCD_CULTIVATED_FIELD
                            for band_name in all_band_names])

                    nlcd_natural_variable_bands = local_band_stack.updateMask(
                        nlcd_natural_mask)
                    nlcd_natural_variable_bands = nlcd_natural_variable_bands.rename([
                        band_name+'-'+NLCD_NATURAL_FIELD
                        for band_name in all_band_names])
                    nlcd_closest_year_image = ee.Image(
                        int(nlcd_closest_year)).rename(NLCD_CLOSEST_YEAR_FIELD)
                    if all_bands is None:
                        all_bands = nlcd_natural_variable_bands
                    else:
                        all_bands = all_bands.addBands(
                            nlcd_natural_variable_bands)
                    all_bands = all_bands.addBands(nlcd_cultivated_variable_bands)
                    all_bands = all_bands.addBands(nlcd_natural_mask)
                    all_bands = all_bands.addBands(nlcd_cultivated_mask)
                    all_bands = all_bands.addBands(nlcd_closest_year_image)
                else:
                    nlcd_cultivated_variable_bands_poly_in = local_band_stack.updateMask(
                        nlcd_cultivated_mask_poly_in)
                    nlcd_cultivated_variable_bands_poly_in = \
                        nlcd_cultivated_variable_bands_poly_in.rename([
                            f'{band_name}-{NLCD_CULTIVATED_FIELD}-{POLY_IN_FIELD}'
                            for band_name in all_band_names])

                    nlcd_natural_variable_bands_poly_in = local_band_stack.updateMask(
                        nlcd_natural_mask_poly_in)
                    nlcd_natural_variable_bands_poly_in = nlcd_natural_variable_bands_poly_in.rename([
                        f'{band_name}-{NLCD_NATURAL_FIELD}-{POLY_IN_FIELD}'
                        for band_name in all_band_names])
                    nlcd_closest_year_image = ee.Image(
                        int(nlcd_closest_year)).rename(NLCD_CLOSEST_YEAR_FIELD)
                    if all_bands is None:
                        all_bands = nlcd_cultivated_variable_bands_poly_in
                    else:
                        all_bands = all_bands.addBands(
                            nlcd_natural_variable_bands_poly_in)
                    all_bands = all_bands.addBands(nlcd_cultivated_variable_bands_poly_in)
                    all_bands = all_bands.addBands(nlcd_natural_mask_poly_in)
                    all_bands = all_bands.addBands(nlcd_cultivated_mask_poly_in)

                    nlcd_cultivated_variable_bands_poly_out = local_band_stack.updateMask(
                        nlcd_cultivated_mask_poly_out)
                    nlcd_cultivated_variable_bands_poly_out = \
                        nlcd_cultivated_variable_bands_poly_out.rename([
                            f'{band_name}-{NLCD_CULTIVATED_FIELD}-{POLY_OUT_FIELD}'
                            for band_name in all_band_names])

                    nlcd_natural_variable_bands_poly_out = local_band_stack.updateMask(
                        nlcd_natural_mask_poly_out)
                    nlcd_natural_variable_bands_poly_out = nlcd_natural_variable_bands_poly_out.rename([
                        f'{band_name}-{NLCD_NATURAL_FIELD}-{POLY_OUT_FIELD}'
                        for band_name in all_band_names])
                    nlcd_closest_year_image = ee.Image(
                        int(nlcd_closest_year)).rename(NLCD_CLOSEST_YEAR_FIELD)
                    all_bands = all_bands.addBands(nlcd_natural_variable_bands_poly_out)
                    all_bands = all_bands.addBands(nlcd_cultivated_variable_bands_poly_out)
                    all_bands = all_bands.addBands(nlcd_natural_mask_poly_out)
                    all_bands = all_bands.addBands(nlcd_cultivated_mask_poly_out)

                    all_bands = all_bands.addBands(nlcd_closest_year_image)

            if corine_flag:
                corine_cultivated_variable_bands = \
                    local_band_stack.updateMask(corine_cultivated_mask.eq(1))
                corine_cultivated_variable_bands = \
                    corine_cultivated_variable_bands.rename([
                        band_name+'-'+CORINE_CULTIVATED_FIELD
                        for band_name in all_band_names])

                corine_natural_variable_bands = local_band_stack.updateMask(
                    corine_natural_mask.eq(1))
                corine_natural_variable_bands = \
                    corine_natural_variable_bands.rename([
                        band_name+'-'+CORINE_NATURAL_FIELD
                        for band_name in all_band_names])
                corine_closest_year_image = ee.Image(
                    int(corine_closest_year)).rename(
                    CORINE_CLOSEST_YEAR_FIELD)
                if all_bands is None:
                    all_bands = corine_cultivated_variable_bands
                else:
                    all_bands = all_bands.addBands(
                        corine_cultivated_variable_bands)
                all_bands = all_bands.addBands(corine_natural_variable_bands)
                all_bands = all_bands.addBands(corine_natural_mask)
                all_bands = all_bands.addBands(corine_cultivated_mask)
                all_bands = all_bands.addBands(corine_closest_year_image)

        print('reduce regions')

        # determine area in/out of point area
        if ee_poly:
            def area_in_out(feature):
                feature_area = feature.area()
                area_in = ee_poly.intersection(feature.geometry()).area()
                return feature.set({
                    POLY_OUT_FIELD: feature_area.subtract(area_in),
                    POLY_IN_FIELD: area_in})

            year_points = year_points.map(area_in_out).getInfo()

        samples = all_bands.reduceRegions(**{
            'collection': year_points,
            'reducer': REDUCER}).getInfo()
        sample_list.extend(samples['features'])

    return header_fields_with_prev_year, sample_list


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

    ee_poly = None
    if args.polygon_path:
        ee_poly = _load_ee_poly(args.polygon_path)

    pts_by_year = _filter_and_buffer_points_by_year(
        point_table, args.lat_field, args.long_field, args.year_field,
        args.point_buffer)

    print('sample modis')



    print('calculating pheno variables')
    header_fields, sample_list = _sample_pheno(
        pts_by_year, args.nlcd, args.corine, ee_poly)

    with open(f'sampled_{args.buffer}m_{landcover_substring}_{os.path.basename(args.csv_path)}', 'w') as table_file:
        table_file.write(
            ','.join(table.columns) + f',{",".join(header_fields)}\n')
        for sample in sample_list:
            table_file.write(','.join([
                str(sample['properties'][key])
                for key in table.columns]) + ',')
            table_file.write(','.join([
                'invalid' if field not in sample['properties']
                else str(sample['properties'][field])
                for field in header_fields]) + '\n')


if __name__ == '__main__':
    main()
