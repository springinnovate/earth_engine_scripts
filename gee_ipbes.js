var datasets = {
    'downstream_bene_2017_50000': 'gs://ecoshard-root/cog/cog_downstream_bene_2017_50000.tif',
    'downstream_bene_2017_500000': 'gs://ecoshard-root/cog/cog_downstream_bene_2017_500000.tif',
    'nutrient_deficit_10s_cur': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_deficit_10s_cur_compressed.tif',
    'nutrient_deficit_10s_ssp1': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_deficit_10s_ssp1.tif',
    'nutrient_deficit_10s_ssp3': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_deficit_10s_ssp3.tif',
    'nutrient_deficit_10s_ssp5': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_deficit_10s_ssp5.tif',
    'nutrient_deficit_change_10s_ssp1': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_deficit_change_10s_ssp1_compressed.tif',
    'nutrient_deficit_change_10s_ssp3': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_deficit_change_10s_ssp3_compressed.tif',
    'nutrient_deficit_change_10s_ssp5': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_deficit_change_10s_ssp5_compressed.tif',
    'nutrient_pop_30s_cur': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_pop_30s_cur_compressed.tif',
    'nutrient_pop_30s_ssp3': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_pop_30s_ssp3.tif',
    'nutrient_pop_30s_ssp5': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_pop_30s_ssp5.tif',
    'nutrient_pop_change_10s_ssp': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_pop_change_10s_ssp_compressed.tif',
    'nutrient_pop_change_30s_ssp1': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_pop_change_30s_ssp1_compressed.tif',
    'nutrient_pop_change_30s_ssp3': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_pop_change_30s_ssp3_compressed.tif',
    'nutrient_pop_change_30s_ssp5': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_nutrient_pop_change_30s_ssp5_compressed.tif',
    'pollination_deficit_10s_cur': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_deficit_10s_cur_compressed.tif',
    'pollination_deficit_10s_ssp1': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_deficit_10s_ssp1.tif',
    'pollination_deficit_10s_ssp3': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_deficit_10s_ssp3.tif',
    'pollination_deficit_10s_ssp5': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_deficit_10s_ssp5.tif',
    'pollination_deficit_change_10s_ssp1': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_deficit_change_10s_ssp1_compressed.tif',
    'pollination_deficit_change_10s_ssp3': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_deficit_change_10s_ssp3_compressed.tif',
    'pollination_deficit_change_10s_ssp5': 'gs://ipbes-natcap-ecoshard-data-for-publication/cog/cog_pollination_deficit_change_10s_ssp5_compressed.tif',
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
        'position': "middle-"+mapside[1]
      }
    });

    var default_control_text = mapside[1]+' controls';
    var controls_label = ui.Label(default_control_text);
    var last_layer = null;
    var select = ui.Select({
      items: Object.keys(datasets),
      onChange: function(key) {
          controls_label.setValue('loading .....');
          select.setDisabled(true);
          if (last_layer !== null) {
            map.remove(map.layers().get(0));
            min_val.setDisabled(true);
            max_val.setDisabled(true);
          }
          var layer = ee.Image.loadGeoTIFF(datasets[key]);

          var mean_reducer = ee.Reducer.percentile([10, 90], ['p10', 'p90']);
          var meanDictionary = layer.reduceRegion({
            reducer: mean_reducer,
            geometry: map.getBounds(true),
            bestEffort: true,
          });

          ee.data.computeValue(meanDictionary, function (val) {
            var visParams = {
              min: val['B0_p10'],
              max: val['B0_p90'],
              palette: ['000000', '005aff', '43c8c8', 'fff700', 'ff0000'],
            };
            map.addLayer(layer, visParams);
            last_layer = layer;
            min_val.setValue(visParams.min, false);
            max_val.setValue(visParams.max, false);
            min_val.setDisabled(false);
            max_val.setDisabled(false);
            controls_label.setValue(default_control_text);
            select.setDisabled(false);
          });
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
    min_val.setDisabled(true);

    var max_val = ui.Textbox(
      100, 100, function (value) {
        visParams.max = +(value);
        updateVisParams();
      });
    max_val.setDisabled(true);

    var point_val = ui.Textbox('nothing clicked');
    function updateVisParams() {
      if (last_layer !== null) {
        map.remove(map.layers().get(0));
        map.addLayer(last_layer, visParams);
      }
    }

    select.setPlaceholder('Choose a dataset...');

    var range_button = ui.Button(
      'Detect Range', function () {
        var mean_reducer = ee.Reducer.percentile([10, 90], ['p10', 'p90']);
        var meanDictionary = last_layer.reduceRegion({
          reducer: mean_reducer,
          geometry: map.getBounds(true),
          bestEffort: true,
        });
        ee.data.computeValue(meanDictionary, function (val) {
          min_val.setValue(val['B0_p10']);
          max_val.setValue(val['B0_p90']);
        });
      });

    panel.add(controls_label);
    panel.add(select);
    panel.add(ui.Label('min'));
    panel.add(min_val);
    panel.add(ui.Label('max'));
    panel.add(max_val);
    panel.add(range_button);
    panel.add(ui.Label('picked point'));
    panel.add(point_val);
    panel_list.push([panel, min_val, max_val]);
    map.add(panel);

    var last_point_layer = null;

    map.setControlVisibility(false);
    map.setControlVisibility({"mapTypeControl": true});
    map.onClick(function (obj) {
      var point = ee.Geometry.Point([obj.lon, obj.lat]);
      if (last_layer !== null) {
        var point_sample = last_layer.sampleRegions({
          collection: point,
          //scale: 10,
          //geometries: true
        });
        ee.data.computeValue(point_sample, function (val) {
          point_val.setValue(val.features[0].properties.B0.toString());
          if (last_point_layer !== null) {
            map.remove(last_point_layer);
          }
          last_point_layer = map.addLayer(point, {'color': '#00FF00'});
        });
      }

      console.log(obj.lat);
      console.log(obj.lon);
      console.log(point_sample);
    })
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
