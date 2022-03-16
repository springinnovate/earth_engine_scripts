var datasets = {
    'coastal_pop_30s_cur': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_coastal_pop_30s_cur.tif',
    'coastal_pop_30s_ssp1': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_coastal_pop_30s_ssp1.tif',
    'coastal_pop_30s_ssp3': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_coastal_pop_30s_ssp3.tif',
    'coastal_pop_30s_ssp5': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_coastal_pop_30s_ssp5.tif',
    'nutrient_deficit_10s_cur_compressed': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_deficit_10s_cur_compressed.tif',
    'nutrient_deficit_10s_ssp1': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_deficit_10s_ssp1.tif',
    'nutrient_deficit_10s_ssp3': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_deficit_10s_ssp3.tif',
    'nutrient_deficit_10s_ssp5': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_deficit_10s_ssp5.tif',
    'nutrient_deficit_change_10s_ssp1_compressed': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_deficit_change_10s_ssp1_compressed.tif',
    'nutrient_deficit_change_10s_ssp3_compressed': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_deficit_change_10s_ssp3_compressed.tif',
    'nutrient_deficit_change_10s_ssp5_compressed': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_deficit_change_10s_ssp5_compressed.tif',
    'nutrient_pop_30s_cur_compressed': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_pop_30s_cur_compressed.tif',
    'nutrient_pop_30s_ssp3': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_pop_30s_ssp3.tif',
    'nutrient_pop_30s_ssp5': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_pop_30s_ssp5.tif',
    'nutrient_pop_change_10s_ssp_compressed': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_pop_change_10s_ssp_compressed.tif',
    'nutrient_pop_change_30s_ssp1_compressed': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_pop_change_30s_ssp1_compressed.tif',
    'nutrient_pop_change_30s_ssp3_compressed': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_pop_change_30s_ssp3_compressed.tif',
    'nutrient_pop_change_30s_ssp5_compressed': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_pop_change_30s_ssp5_compressed.tif',
    'pollination_deficit_10s_cur_compressed': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_deficit_10s_cur_compressed.tif',
    'pollination_deficit_10s_ssp1': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_deficit_10s_ssp1.tif',
    'pollination_deficit_10s_ssp3': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_deficit_10s_ssp3.tif',
    'pollination_deficit_10s_ssp5': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_deficit_10s_ssp5.tif',
    'pollination_deficit_change_10s_ssp1_compressed': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_deficit_change_10s_ssp1_compressed.tif',
    'pollination_deficit_change_10s_ssp3_compressed': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_deficit_change_10s_ssp3_compressed.tif',
    'pollination_deficit_change_10s_ssp5_compressed': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_deficit_change_10s_ssp5_compressed.tif',
    'pollination_pop_30s_cur': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_pop_30s_cur.tif',
    'pollination_pop_30s_ssp1': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_pop_30s_ssp1.tif',
    'pollination_pop_30s_ssp3': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_pop_30s_ssp3.tif',
    'pollination_pop_30s_ssp5': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_pop_30s_ssp5.tif',
    'pollination_pop_change_30s_ssp1': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_pop_change_30s_ssp1.tif',
    'pollination_pop_change_30s_ssp3': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_pop_change_30s_ssp3.tif',
    'pollination_pop_change_30s_ssp5': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_pop_change_30s_ssp5.tif',
    'pop_change_nutrient_30s_ssp1': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pop_change_nutrient_30s_ssp1.tif',
    'pop_change_nutrient_30s_ssp3': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pop_change_nutrient_30s_ssp3.tif',
    'pop_change_nutrient_30s_ssp5': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pop_change_nutrient_30s_ssp5.tif',
    'water_ruralpop_30s_2015': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_water_ruralpop_30s_2015.tif',
    'water_ruralpop_30s_ssp1': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_water_ruralpop_30s_ssp1.tif',
    'water_ruralpop_30s_ssp3': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_water_ruralpop_30s_ssp3.tif',
    'water_ruralpop_30s_ssp5': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_water_ruralpop_30s_ssp5.tif',
};
Map.drawingTools().setShown(false);
var linkedMap = ui.Map();
var linker = ui.Map.Linker([ui.root.widgets().get(0), linkedMap]);
// Create a SplitPanel which holds the linked maps side-by-side.
var splitPanel = ui.SplitPanel({
  firstPanel: linker.get(0),
  secondPanel: linker.get(1),
  orientation: 'horizontal',
  wipe: true,
  style: {stretch: 'both'}
});
ui.root.widgets().reset([splitPanel]);

var panel_list = [];
[[Map, 'left'], [linkedMap, 'right']].forEach(function(mapside, index) {
    var map = mapside[0];
    var panel = ui.Panel({
      layout: ui.Panel.Layout.flow('vertical'),
      style: {
        'position': 'top-'+mapside[1],
        width: '300px'}
    });

    var last_layer = null;
    var select = ui.Select({
      items: Object.keys(datasets),
      onChange: function(key) {
          if (last_layer !== null) {
            map.remove(map.layers().get(0));
          }
          var layer = ee.Image.loadGeoTIFF(datasets[key]);
          map.addLayer(layer, visParams);
          last_layer = layer;
          console.log(datasets[key]);
      }
    });

    var visParams = {
      min: 0.0,
      max: 100.0,
      palette: ['000000', '005aff', '43c8c8', 'fff700', 'ff0000'],
    };

    var min_val = ui.Textbox(
      0, 0, function (value) {
        visParams.min = +(value);
        updateVisParams();
      });

    var max_val = ui.Textbox(
      100, 100, function (value) {
        visParams.max = +(value);
        updateVisParams();
      });

    function updateVisParams() {
      if (last_layer !== null) {
        map.remove(map.layers().get(0));
        map.addLayer(last_layer, visParams);
      }
    }

    select.setPlaceholder('Choose a location...');

    var range_button = ui.Button(
      'Detect Range', function () {
        var mean_reducer = ee.Reducer.percentile([10, 90], ['p10', 'p90']);
        var meanDictionary = last_layer.reduceRegion({
          reducer: mean_reducer,
          geometry: map.getBounds(true),
          bestEffort: true,
        });
        ee.data.computeValue(meanDictionary.get('B0_p10'), function (val) {
          min_val.setValue(val);
        });
        ee.data.computeValue(meanDictionary.get('B0_p90'), function (val) {
          max_val.setValue(val);
        });

      });

    panel.add(select);
    panel.add(min_val);
    panel.add(max_val);
    panel.add(range_button);
    panel_list.push([panel, min_val, max_val]);
    map.add(panel);

    map.setControlVisibility(
      {"zoomControl": false});

});

var clone_to_right = ui.Button(
  'Use this range in both windows', function () {
      panel_list[1][1].setValue(panel_list[0][1].getValue())
      panel_list[1][2].setValue(panel_list[0][2].getValue())
});
var clone_to_left = ui.Button(
  'Use this range in both windows', function () {
      panel_list[0][1].setValue(panel_list[1][1].getValue())
      panel_list[0][2].setValue(panel_list[1][2].getValue())
});

panel_list[0][0].add(clone_to_right);
panel_list[1][0].add(clone_to_left);

