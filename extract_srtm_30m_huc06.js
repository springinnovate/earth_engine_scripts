var dataset = ee.Image('USGS/SRTMGL1_003');
var elevation = dataset.select('elevation');
//Map.setCenter(-112.8598, 36.2841, 10);

// Load watersheds from a data table.
var sheds = ee.FeatureCollection('USGS/WBD/2017/HUC06')
  // Convert 'areasqkm' property from string to number.
  .map(function(feature){
    var num = ee.Number.parse(feature.get('areasqkm'));
    return feature.set('areasqkm', num);
  });

// Define a region roughly covering the continental US.
var continentalUSbb = ee.Geometry.Rectangle(-127.18, 19.39, -62.75, 51.29);

// Filter the table geographically: only watersheds in the continental US.
var us_watersheds = sheds.filterBounds(continentalUSbb);

//Map.addLayer(us_watersheds);

elevation = elevation.clipToCollection(us_watersheds);

Map.addLayer(elevation, {min: 0, max: 5000}, 'ele');

//Map.setCenter(7.82, 49.1, 4);

var label = 'SRTM_30m_US_huc06';

var bucket = 'ecoshard-root';
Export.image.toCloudStorage(
  {
    'image': elevation,
    'description': label,
    'bucket': bucket,
    'fileNamePrefix': 'gee_export/'+label,
    'scale':30,
    'region': continentalUSbb,
    'crs': "EPSG:4326",
    'maxPixels': 1e12,
});
