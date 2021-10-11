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

    img = ee.ImageCollection("LANDSAT/LT05/C01/T1_8DAY_NDVI").filterDate('2014-01-01', '2015-01-01').mean()

    # Define the urban location of interest as a point near Lyon, France.
    u_lon = 4.8148
    u_lat = 45.7758
    u_poi = ee.Geometry.Point(u_lon, u_lat)

    # Define the rural location of interest as a point away from the city.
    r_lon = 5.175964
    r_lat = 45.574064
    r_poi = ee.Geometry.Point(r_lon, r_lat)


    pts = ee.FeatureCollection([
      ee.Feature(ee.Geometry.Point([-118.6010, 37.0777]), {'plot_id': 1}),
      ee.Feature(ee.Geometry.Point([-118.5896, 37.0778]), {'plot_id': 2}),
      ee.Feature(ee.Geometry.Point([-118.5842, 37.0805]), {'plot_id': 3}),
      ee.Feature(ee.Geometry.Point([-118.5994, 37.0936]), {'plot_id': 4}),
      ee.Feature(ee.Geometry.Point([-118.5861, 37.0567]), {'plot_id': 5})
    ])

    #img = img.addBands(elv)

    #samples = img.reduceRegions(**{
    #    'collection': pts,
    #    'scale': 30,
    #    'crs': 'EPSG:4326'})
    buffer_pts = pts.map(buffer_points(45))
    samples = img.sample(region=buffer_pts, scale=30, projection='EPSG:4326')
    print(samples.getInfo())


    print(f'ndvi val: {ndvi_point}')
    ndvi_point = img.mean().sample(u_poi, scale=0.001, projection='EPSG:4326').first().get('NDVI').getInfo()

    # Print the elevation near Lyon, France.
    elv_urban_point = elv.sample(u_poi, scale).first().get('elevation').getInfo()
    print('Ground elevation at urban point:', elv_urban_point, 'm')

    # Calculate and print the mean value of the LST collection at the point.
    lst_urban_point = lst.mean().sample(u_poi, scale).first().get('LST_Day_1km').getInfo()
    print('Average daytime LST at urban point:', round(lst_urban_point*0.02 -273.15, 2), '°C')

    # Print the land cover type at the point.
    lc_urban_point = lc.first().sample(u_poi, scale).first().get('LC_Type1').getInfo()
    print('Land cover value at urban point is:', lc_urban_point)


    return


    v = img.sample(ee.Geometry.Point(-118.6010, 37.077), 1000)
    print(v.first().get('NDVI').getInfo())
    return

    for sample in samples:
        print(sample)


if __name__ == '__main__':
    main()
