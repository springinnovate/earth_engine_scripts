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
Map.setCenter(0, 0, 2);
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
    map.style().set('cursor', 'crosshair');
    var panel = ui.Panel({
      layout: ui.Panel.Layout.flow('vertical'),
      style: {
        'position': "middle-"+mapside[1],
        'backgroundColor': 'rgba(255, 255, 255, 0.4)'
      }
    });

    var default_control_text = mapside[1]+' controls';
    var controls_label = ui.Label({
      value: default_control_text,
      style: {
        backgroundColor: 'rgba(0, 0, 0, 0)',
      }
    });
    var active_map = {
      'last_layer': null,
      'raster': null,
      'point_val': null,
      'last_point_layer': null,
      'map': map,
    };
    var select = ui.Select({
      items: Object.keys(datasets),
      onChange: function(key, self) {
          self.setDisabled(true);
          var original_value = self.getValue();
          self.setPlaceholder('loading ...');
          self.setValue(null, false);
          if (active_map.last_layer !== null) {
            map.remove(active_map.last_layer);
            min_val.setDisabled(true);
            max_val.setDisabled(true);
          }
          active_map.raster = ee.Image.loadGeoTIFF(datasets[key]);

          var mean_reducer = ee.Reducer.percentile([10, 90], ['p10', 'p90']);
          var meanDictionary = active_map.raster.reduceRegion({
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
            active_map.last_layer = map.addLayer(
              active_map.raster, visParams);
            min_val.setValue(visParams.min, false);
            max_val.setValue(visParams.max, false);
            min_val.setDisabled(false);
            max_val.setDisabled(false);
            self.setValue(original_value, false);
            self.setDisabled(false);
          });
      }
    });

    var palette_array = ['000000', '005aff', '43c8c8', 'fff700', 'ff0000'];
    var visParams = {
      min: 0.0,
      max: 100.0,
      palette: palette_array,
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

    active_map.point_val = ui.Textbox('nothing clicked');
    function updateVisParams() {
      if (active_map.last_layer !== null) {
        active_map.last_layer.setVisParams(visParams);
      }
    }

    select.setPlaceholder('Choose a dataset...');
    var range_button = ui.Button(
      'Detect Range', function (self) {
        self.setDisabled(true);
        var base_label = self.getLabel();
        self.setLabel('Detecting...');
        var mean_reducer = ee.Reducer.percentile([10, 90], ['p10', 'p90']);
        var meanDictionary = active_map.raster.reduceRegion({
          reducer: mean_reducer,
          geometry: map.getBounds(true),
          bestEffort: true,
        });
        ee.data.computeValue(meanDictionary, function (val) {
          min_val.setValue(val['B0_p10'], false);
          max_val.setValue(val['B0_p90'], true);
          self.setLabel(base_label)
          self.setDisabled(false);
        });
      });

    panel.add(controls_label);
    panel.add(select);
    panel.add(ui.Label({
        value: 'min',
        style:{'backgroundColor': 'rgba(0, 0, 0, 0)'}
      }));
    panel.add(min_val);
    panel.add(ui.Label({
        value: 'max',
        style:{'backgroundColor': 'rgba(0, 0, 0, 0)'}
      }));
    panel.add(max_val);
    panel.add(range_button);
    panel.add(ui.Label({
      value: 'picked point',
      style: {'backgroundColor': 'rgba(0, 0, 0, 0)'}
    }));
    panel.add(active_map.point_val);
    panel_list.push([panel, min_val, max_val, map, active_map]);
    map.add(panel);

    var legend_panel = ui.Panel({
      layout: ui.Panel.Layout.Flow('horizontal'),
      style: {
        position: 'top-center',
        padding: '0px',
        backgroundColor: 'rgba(255, 255, 255, 0.4)'
      }
    });

    var makeRow = function(color, name) {
      var colorBox = ui.Label({
        style: {
          backgroundColor: '#' + color,
          padding: '4px 25px 4px 25px',
          margin: '0 0 0px 0',
          position: 'bottom-center',
        }
      });
      var description = ui.Label({
        value: name,
        style: {
          margin: '0 0 0px 0px',
          position: 'top-center',
          fontSize: '10px',
          padding: 0,
          border: 0,
          textAlign: 'center',
          backgroundColor: 'rgba(0, 0, 0, 0)',
        }
      });

      return ui.Panel({
        widgets: [colorBox, description],
        layout: ui.Panel.Layout.Flow('vertical'),
        style: {
          backgroundColor: 'rgba(0, 0, 0, 0)',
        }
      });
    };

    var names = ['Low', '', '', '', 'High'];

    // Add color and and names
    for (var i = 0; i<5; i++) {
      legend_panel.add(makeRow(palette_array[i], names[i]));
      }
    map.add(legend_panel);

    var last_point_layer = null;

    map.setControlVisibility(false);
    map.setControlVisibility({"mapTypeControl": true});

});

var clone_to_right = ui.Button(
  'Use this range in both windows', function () {
      panel_list[1][1].setValue(panel_list[0][1].getValue(), false)
      panel_list[1][2].setValue(panel_list[0][2].getValue(), true)
});
var clone_to_left = ui.Button(
  'Use this range in both windows', function () {
      panel_list[0][1].setValue(panel_list[1][1].getValue(), false)
      panel_list[0][2].setValue(panel_list[1][2].getValue(), true)
});

//panel_list.push([panel, min_val, max_val, map, active_map]);
panel_list.forEach(function (panel_array) {
  var map = panel_array[3];
  map.onClick(function (obj) {
    var point = ee.Geometry.Point([obj.lon, obj.lat]);
    [panel_list[0][4], panel_list[1][4]].forEach(function (active_map) {
      if (active_map.last_layer !== null) {
        active_map.point_val.setValue('sampling...')
        var point_sample = active_map.raster.sampleRegions({
          collection: point,
          //scale: 10,
          //geometries: true
        });
        ee.data.computeValue(point_sample, function (val) {
          if (val.features.length > 0) {
            active_map.point_val.setValue(val.features[0].properties.B0.toString());
            if (active_map.last_point_layer !== null) {
              active_map.map.remove(active_map.last_point_layer);
            }
            active_map.last_point_layer = active_map.map.addLayer(
              point, {'color': '#FF00FF'});
          } else {
            active_map.point_val.setValue('nodata');
          }
        });
      }
    });
  });
});

panel_list[0][0].add(clone_to_right);
panel_list[1][0].add(clone_to_left);
