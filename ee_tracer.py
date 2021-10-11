"""EE tracer code."""
import os

import ee
import pandas

CSV_PATH = 'cotton_site_info.csv'

DATASET = 'LANDSAT/LT05/C01/T1_8DAY_NDVI'
START_DATE = '1997-01-01'
END_DATE = '2019-01-01'

HEADER_FIELD = f'{DATASET}_{START_DATE}_{END_DATE}'


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

    img = ee.ImageCollection("LANDSAT/LT05/C01/T1_8DAY_NDVI").filterDate('1997-01-01', '2019-01-01')
    mean_img = img.reduce(ee.Reducer.mean())
    print('starting google earth engine sample')
    REDUCER = 'first'
    samples = mean_img.reduceRegions(**{
        'collection': pts,
        'scale': 30,
        'reducer': REDUCER}).getInfo()
    with open(f'sampled_{os.path.basename(CSV_PATH)}', 'w') as table_file:
        table_file.write(','.join(table.columns) + f',{HEADER_FIELD}\n')
        for sample in samples['features']:
            table_file.write(','.join([
                str(sample['properties'][key]) for key in table.columns]) +
                f",{sample['properties'][REDUCER]}\n")


if __name__ == '__main__':
    main()
