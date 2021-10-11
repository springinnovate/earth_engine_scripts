"""EE tracer code."""
import ee


def buffer_points(radius):
    def _buffer_points(pt):
        pt = ee.Feature(pt)
        return pt.buffer(radius).bounds()
    return _buffer_points


def main():
    """Entry point."""
    ee.Initialize()

    # Import the MODIS land cover collection.
    lc = ee.ImageCollection('MODIS/006/MCD12Q1')

    # Import the MODIS land surface temperature collection.
    lst = ee.ImageCollection('MODIS/006/MOD11A1')

    # Import the USGS ground elevation image.
    elv = ee.Image('USGS/SRTMGL1_003')

    # Initial date of interest (inclusive).
    i_date = '2017-01-01'

    # Final date of interest (exclusive).
    f_date = '2020-01-01'

    # Selection of appropriate bands and dates for LST.
    lst = lst.select('LST_Day_1km', 'QC_Day').filterDate(i_date, f_date)

    img = ee.ImageCollection("LANDSAT/LT05/C01/T1_8DAY_NDVI").filterDate('1997-01-01', '2019-01-01')

    pts = ee.FeatureCollection([
      ee.Feature(ee.Geometry.Point([-118.6010, 37.0777]), {'plot_id': 1}),
      ee.Feature(ee.Geometry.Point([-118.5896, 37.0778]), {'plot_id': 2}),
      ee.Feature(ee.Geometry.Point([-118.5842, 37.0805]), {'plot_id': 3}),
      ee.Feature(ee.Geometry.Point([-118.5994, 37.0936]), {'plot_id': 4}),
      ee.Feature(ee.Geometry.Point([-118.5861, 37.0567]), {'plot_id': 5})
    ])

    mean_img = img.reduce(ee.Reducer.mean())
    samples = mean_img.reduceRegions(**{
        'collection': pts,
        'scale': 30,
        'reducer': 'mean'}).getInfo()
    print('geometry,LANDSAT/LT05/C01/T1_8DAY_NDVI_mean')
    for sample in samples['features']:
        print(f"{sample['geometry']['coordinates']}, {sample['properties']['mean']}")


if __name__ == '__main__':
    main()
