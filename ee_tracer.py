"""EE tracer code."""
import os

import ee
import pandas

CSV_PATH = 'cotton_site_info.csv'


def main():
    """Entry point."""
    ee.Initialize()
    table = pandas.read_csv(CSV_PATH)

    pts = ee.FeatureCollection([
        ee.Feature(
            ee.Geometry.Point(row['long'], row['lat']),
            row.to_dict())
        for index, row in table.dropna().iterrows() if index == 1])
    print(pts)

    img = ee.ImageCollection("LANDSAT/LT05/C01/T1_8DAY_NDVI").filterDate('1997-01-01', '2019-01-01')
    mean_img = img.reduce(ee.Reducer.mean())
    print('starting google earth engine sample')
    samples = mean_img.reduceRegions(**{
        'collection': pts,
        'scale': 30,
        'reducer': 'first'}).getInfo()
    with open(f'sampled_{os.path.basename(CSV_PATH)}', 'w') as table_file:
        table_file.write(','.join(table.columns) + '\n')
        for sample in samples['features']:
            table_file.write(','.join([
                str(sample['properties'][key]) for key in table.columns])+'\n')


if __name__ == '__main__':
    main()
