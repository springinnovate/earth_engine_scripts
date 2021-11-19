"""EE tracer code."""
from datetime import datetime
import os

import ee
import pandas

CSV_PATH = 'data_table_citrusformatics_MKL.csv'
LONG_FIELD = 'field_longitude'
LAT_FIELD = 'field_latitude'
REDUCER = 'mean'


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
    all_bands = None
    header_field_offset = 0
    for year in range(start_year, end_year+1):
        print(f'processing year {year}')
        header_fields.extend([
            f'{DATASET_NAME}-{year}-{field}'
            for field in julian_day_variables+raw_variables])
        print(header_fields)
        current_year = datetime.strptime(f'{year}-01-01', "%Y-%m-%d")
        days_since_epoch = (current_year - epoch_date).days
        modis_band_names = header_fields[
            header_field_offset:header_field_offset+len(julian_day_variables)]
        print(modis_band_names)
        bands_since_1970 = modis_phen.select(
            julian_day_variables).filterDate(
            f'{year}-01-01', f'{year}-12-31')
        julian_day_bands = (
            bands_since_1970.toBands()).subtract(days_since_epoch)
        julian_day_bands = julian_day_bands.rename(modis_band_names)
        if all_bands is None:
            all_bands = julian_day_bands
        else:
            all_bands = all_bands.addBands(julian_day_bands)
        raw_band_names = header_fields[
            header_field_offset+len(julian_day_variables)::]
        raw_variable_bands = modis_phen.select(
            raw_variables).filterDate(
            f'{year}-01-01', f'{year}-12-31').toBands()
        raw_variable_bands = raw_variable_bands.rename(raw_band_names)
        print(raw_band_names)
        all_bands = all_bands.addBands(raw_variable_bands)
        header_field_offset = len(header_fields)
        print(header_field_offset)

    samples = all_bands.reduceRegions(**{
        'collection': pts,
        'scale': 2000,
        'reducer': REDUCER}).getInfo()
    print(samples['features'][0])
    return header_fields, samples['features']


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
    header_fields, sample_list = _sample_pheno(pts, 2008, 2017)
    print(header_fields)
    print(len(sample_list[0]))
    with open(f'sampled_{os.path.basename(CSV_PATH)}', 'w') as table_file:
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
