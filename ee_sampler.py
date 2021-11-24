"""EE tracer code."""
from datetime import datetime
import os

import ee
import numpy
import pandas

CSV_PATH = 'data_table_citrusformatics_MKL.csv'
YEAR_FIELD = 'crop_year'
LONG_FIELD = 'field_longitude'
LAT_FIELD = 'field_latitude'
REDUCER = 'mean'
BUFFER = 2000
NLCD_DATASET = 'USGS/NLCD_RELEASES/2016_REL'
NLCD_VALID_YEARS = numpy.array([
    1992, 2001, 2004, 2006, 2008, 2011, 2013, 2016])
NLCD_CLOSEST_YEAR_FIELD = 'NLCD-year'
NLCD_NATURAL_FIELD = 'NLCD-natural'
NLCD_CULTIVATED_FIELD = 'NLCD-cultivated'

COOPERNICUS_DATASET = 'COPERNICUS/CORINE/V20/100m'
COOPERNICUS_VALID_YEARS = numpy.array([1990, 2000, 2006, 2012, 2018])
COOPERNICUS_CLOSEST_YEAR_FIELD = 'COOPERNICUS-year'
COOPERNICUS_NATURAL_FIELD = 'COOPERNICUS-natural'
COOPERNICUS_CULTIVATED_FIELD = 'COOPERNICUS-cultivated'

PREV_YEAR_TAG = '-prev-year'


def _get_closest_num(number_list, candidate):
    """Return closest number in sorted list."""
    index = numpy.searchsorted(number_list, candidate)
    if index == len(number_list):
        index -= 1
    closest_candidate = str(number_list[index])
    return closest_candidate


def _coopernicus_natural_cultivated_mask(year):
    """Natural: 311-423, Cultivated: 211 - 244."""
    print(year)
    closest_year = _get_closest_num(COOPERNICUS_VALID_YEARS, year)
    coopernicus_dataset = ee.ImageCollection(
        COOPERNICUS_DATASET)
    #coopernicus_landcover = coopernicus_dataset.select(
    #    'landcover').select('landcover').toBands()

    coopernicus_landcover = coopernicus_dataset.filter(
        ee.Filter.eq('system:index', closest_year)).first().select('landcover')

    natural_mask = ee.Image(0).where(
        coopernicus_landcover.gte(311).And(coopernicus_landcover.lte(423)), 1)
    natural_mask = natural_mask.rename(COOPERNICUS_NATURAL_FIELD)

    cultivated_mask = ee.Image(0).where(
        coopernicus_landcover.gte(211).And(coopernicus_landcover.lte(244)), 1)
    cultivated_mask = cultivated_mask.rename(COOPERNICUS_CULTIVATED_FIELD)
    return natural_mask, cultivated_mask, closest_year


def _nlcd_natural_cultivated_mask(year):
    """Natural for NLCD in 41-74 or 90-95."""
    closest_year = _get_closest_num(NLCD_VALID_YEARS, year)
    nlcd_dataset = ee.ImageCollection(NLCD_DATASET)
    nlcd_year = nlcd_dataset.filter(
        ee.Filter.eq('system:index', closest_year)).first().select('landcover')
    # natural 41-74 & 90-95
    natural_mask = ee.Image(0).where(
        nlcd_year.gte(41).And(nlcd_year.lte(74)).Or(
            nlcd_year.gte(90).And(nlcd_year.lte(95))), 1)
    natural_mask = natural_mask.rename(NLCD_NATURAL_FIELD)

    cultivated_mask = ee.Image(0).where(
        nlcd_year.gte(81).And(nlcd_year.lte(82)), 1)
    cultivated_mask = cultivated_mask.rename(NLCD_CULTIVATED_FIELD)
    return natural_mask, cultivated_mask, closest_year


def _sample_pheno(pts_by_year):
    """Sample phenology variables from https://docs.google.com/spreadsheets/d/1nbmCKwIG29PF6Un3vN6mQGgFSWG_vhB6eky7wVqVwPo"""
    DATASET_NAME = 'MODIS/006/MCD12Q2'  # 500m resolution
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
    modis_phen = ee.ImageCollection(DATASET_NAME)

    header_fields = [
        f'{DATASET_NAME}-{field}'
        for field in julian_day_variables+raw_variables]

    header_fields_with_prev_year = [
        x for field in header_fields
        for x in (
            field, field+PREV_YEAR_TAG,
            field+NLCD_NATURAL_FIELD, field+PREV_YEAR_TAG+NLCD_NATURAL_FIELD,
            field+NLCD_CULTIVATED_FIELD,
            field+PREV_YEAR_TAG+NLCD_CULTIVATED_FIELD,
            field+COOPERNICUS_CULTIVATED_FIELD,
            field+PREV_YEAR_TAG+COOPERNICUS_CULTIVATED_FIELD)]
    header_fields_with_prev_year.append(NLCD_NATURAL_FIELD)
    header_fields_with_prev_year.append(NLCD_CULTIVATED_FIELD)
    header_fields_with_prev_year.append(NLCD_CLOSEST_YEAR_FIELD)
    header_fields_with_prev_year.append(COOPERNICUS_NATURAL_FIELD)
    header_fields_with_prev_year.append(COOPERNICUS_CULTIVATED_FIELD)
    header_fields_with_prev_year.append(COOPERNICUS_CLOSEST_YEAR_FIELD)

    sample_list = []
    for year in pts_by_year.keys():
        print(f'processing year {year}')
        year_points = pts_by_year[year]
        print(type(year_points))
        all_bands = None

        nlcd_natural_mask, nlcd_cultivated_mask, nlcd_closest_year = \
            _nlcd_natural_cultivated_mask(year)

        coopernicus_natural_mask, coopernicus_cultivated_mask, coopernicus_closest_year = \
            _coopernicus_natural_cultivated_mask(year)

        for active_year, band_name_suffix in (
                (year, ''), (year-1, PREV_YEAR_TAG)):
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

            # mask raw variable bands by cultivated/natural
            nlcd_cultivated_variable_bands = local_band_stack.updateMask(
                nlcd_cultivated_mask.eq(1))
            nlcd_cultivated_variable_bands = \
                nlcd_cultivated_variable_bands.rename([
                    band_name+NLCD_CULTIVATED_FIELD
                    for band_name in all_band_names])

            nlcd_natural_variable_bands = local_band_stack.updateMask(
                nlcd_natural_mask.eq(1))
            nlcd_natural_variable_bands = nlcd_natural_variable_bands.rename([
                band_name+NLCD_NATURAL_FIELD
                for band_name in all_band_names])

            coopernicus_cultivated_variable_bands = \
                local_band_stack.updateMask(coopernicus_cultivated_mask.eq(1))
            coopernicus_cultivated_variable_bands = \
                coopernicus_cultivated_variable_bands.rename([
                    band_name+COOPERNICUS_CULTIVATED_FIELD
                    for band_name in all_band_names])

            coopernicus_natural_variable_bands = local_band_stack.updateMask(
                coopernicus_natural_mask.eq(1))
            coopernicus_natural_variable_bands = \
                coopernicus_natural_variable_bands.rename([
                    band_name+COOPERNICUS_NATURAL_FIELD
                    for band_name in all_band_names])

            if all_bands is None:
                all_bands = local_band_stack
            else:
                all_bands = all_bands.addBands(local_band_stack)
            all_bands = all_bands.addBands(nlcd_cultivated_variable_bands)
            all_bands = all_bands.addBands(nlcd_natural_variable_bands)
            all_bands = all_bands.addBands(coopernicus_cultivated_variable_bands)
            all_bands = all_bands.addBands(coopernicus_natural_variable_bands)

            # mask raw variable bands by natural

        print('append bands')

        nlcd_closest_year_image = ee.Image(
            int(nlcd_closest_year)).rename(NLCD_CLOSEST_YEAR_FIELD)
        coopernicus_closest_year_image = ee.Image(
            int(coopernicus_closest_year)).rename(
            COOPERNICUS_CLOSEST_YEAR_FIELD)
        all_bands = all_bands.addBands(nlcd_natural_mask)
        all_bands = all_bands.addBands(nlcd_cultivated_mask)
        all_bands = all_bands.addBands(nlcd_closest_year_image)
        all_bands = all_bands.addBands(coopernicus_natural_mask)
        all_bands = all_bands.addBands(coopernicus_cultivated_mask)
        all_bands = all_bands.addBands(coopernicus_closest_year_image)
        print('reduce regions')
        samples = all_bands.reduceRegions(**{
            'collection': year_points,
            'reducer': REDUCER}).getInfo()
        sample_list.extend(samples['features'])
    print(sample_list[0])
    return header_fields_with_prev_year, sample_list


def main():
    """Entry point."""
    ee.Initialize()
    table = pandas.read_csv(CSV_PATH)
    print(table[YEAR_FIELD].unique())

    print(f'reading points from {CSV_PATH}')
    pts_by_year = {}
    for year in table[YEAR_FIELD].unique():
        pts_by_year[year] = ee.FeatureCollection([
            ee.Feature(
                ee.Geometry.Point(row[LONG_FIELD], row[LAT_FIELD]).buffer(BUFFER),
                row.to_dict())
            for index, row in table[
                table[YEAR_FIELD] == year].dropna().iterrows()])

    print('calculating pheno variables')
    header_fields, sample_list = _sample_pheno(pts_by_year)
    print(header_fields)
    print(len(sample_list[0]))
    with open(f'sampled_{BUFFER}m_{os.path.basename(CSV_PATH)}', 'w') as table_file:
        table_file.write(
            ','.join(table.columns) + f',{",".join(header_fields)}\n')
        for sample in sample_list:
            table_file.write(','.join([
                str(sample['properties'][key])
                for key in table.columns]) + ',')
            table_file.write(','.join([
                str(sample['properties'][field])
                for field in header_fields]) + '\n')


if __name__ == '__main__':
    main()
