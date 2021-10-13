"""EE tracer code."""
from datetime import datetime
import os

import ee
import pandas

CSV_PATH = 'cotton_site_info.csv'

DATASET = 'LANDSAT/LT05/C01/T1_8DAY_NDVI'
START_DATE = '1997-01-01'
END_DATE = '2019-01-01'

HEADER_FIELD = f'{DATASET}_{START_DATE}_{END_DATE}'

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


def main():
    """Entry point."""
    ee.Initialize()
    table = pandas.read_csv(CSV_PATH)

    print(f'reading points from {CSV_PATH}')
    pts = ee.FeatureCollection([
        ee.Feature(
            ee.Geometry.Point(row['long'], row['lat']),
            row.to_dict())
        for index, row in table.dropna().iterrows()])

    print('calculating greenup')
    header_fields, sample_list = _greenup_1(pts, 2001, 2019)
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
