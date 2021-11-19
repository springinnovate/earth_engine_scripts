"""EE tracer code."""
from datetime import datetime
import os

import ee
import pandas

CSV_PATH = 'data_table_citrusformatics_MKL.csv'
LONG_FIELD = 'field_longitude'
LAT_FIELD = 'field_latitude'
REDUCER = 'first'


def _greenup_1(pts, start_year, end_year):
    """Calculate greenup from points at from start to end year inclusive."""
    DATSET_NAME = "MODIS/006/MCD12Q2"
    epoch_date = datetime.strptime('1970-01-01', "%Y-%m-%d")
    modis_phen = ee.ImageCollection(DATSET_NAME)
    header_fields = []
    sample_list = []
    for year in range(start_year, end_year+1):
        print(f'processing year {year}')
        header_fields.append(f'{DATSET_NAME}-{year}')
        current_year = datetime.strptime(f'{year}-01-01', "%Y-%m-%d")
        days_since_epoch = (current_year - epoch_date).days
        current_year_greenup = modis_phen.select('Greenup_1').filterDate(
            f'{year}-01-01', f'{year}-12-31')
        img_year = (current_year_greenup.toBands()).subtract(days_since_epoch)
        samples = img_year.reduceRegions(**{
            'collection': pts,
            'scale': 30,
            'reducer': REDUCER}).getInfo()
        sample_list.append(samples['features'])
    return header_fields, sample_list


def _sample_pheno(pts, start_year, end_year):
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
    header_fields = []
    sample_list = []
    for year in range(start_year, end_year+1):
        print(f'processing year {year}')
        header_fields.extend([
            f'{DATASET_NAME}-{year}-{field}'
            for field in julian_day_variables+raw_variables])
        current_year = datetime.strptime(f'{year}-01-01', "%Y-%m-%d")
        days_since_epoch = (current_year - epoch_date).days
        bands_since_1970 = modis_phen.select(julian_day_variables).filterDate(
            f'{year}-01-01', f'{year}-12-31')
        julian_day_bands = (
            bands_since_1970.toBands()).subtract(days_since_epoch)
        print(type(julian_day_bands))
        raw_variable_bands = modis_phen.select(raw_variables).filterDate(
            f'{year}-01-01', f'{year}-12-31').toBands()
        print(type(raw_variable_bands))

        all_bands = raw_variable_bands.addBands(julian_day_bands)

        samples = all_bands.reduceRegions(**{
            'collection': pts,
            'scale': 30,
            'reducer': REDUCER}).getInfo()
        sample_list.append(samples['features'])
    return header_fields, sample_list

def main():
    """Entry point."""
    ee.Initialize()
    table = pandas.read_csv(CSV_PATH)

    print(f'reading points from {CSV_PATH}')
    pts = ee.FeatureCollection([
        ee.Feature(
            ee.Geometry.Point(row[LONG_FIELD], row[LAT_FIELD]),
            row.to_dict())
        for index, row in table.dropna().iterrows()])

    print('calculating pheno variables')
    header_fields, sample_list = _sample_pheno(pts, 2001, 2019)
    print(header_fields)
    with open(f'sampled_{os.path.basename(CSV_PATH)}', 'w') as table_file:
        table_file.write(
            ','.join(table.columns) + f',{",".join(header_fields)}\n')
        for individual_samples in zip(*sample_list):
            table_file.write(','.join([
                str(individual_samples[0]['properties'][key])
                for key in table.columns]) + ',')
            table_file.write(','.join([
                str('n/a' if REDUCER not in sample['properties'] else sample['properties'][REDUCER])
                for sample in individual_samples]) + '\n')


if __name__ == '__main__':
    main()
