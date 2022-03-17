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

var legend_styles = {
  'black_to_red': ['000000', '005aff', '43c8c8', 'fff700', 'ff0000'],
};
var default_legend_style = 'black_to_red';

function changeColorScheme(key) {
  panel_list[0][3].visParams.legend_palette = legend_styles[key];
  panel_list[0][3].updateVisParams();
  panel_list[1][3].visParams.legend_palette = legend_styles[key];
  panel_list[1][3].updateVisParams();
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
    var active_context = {
      'last_layer': null,
      'raster': null,
      'point_val': null,
      'last_point_layer': null,
      'map': mapside[0],
      'legend_panel': null,
      'visParams': null,
    };

    active_context.map.style().set('cursor', 'crosshair');

    var legend_select = ui.Select({
      items: Object.keys(legend_styles),
      placeholder: default_legend_style,
      onChange: function(key, self) {
        changeColorScheme(key);
    }});

    active_context.visParams = {
      min: 0.0,
      max: 100.0,
      palette: legend_styles[default_legend_style],
    };

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
    var select = ui.Select({
      items: Object.keys(datasets),
      onChange: function(key, self) {
          self.setDisabled(true);
          var original_value = self.getValue();
          self.setPlaceholder('loading ...');
          self.setValue(null, false);
          if (active_context.last_layer !== null) {
            active_context.map.remove(active_context.last_layer);
            min_val.setDisabled(true);
            max_val.setDisabled(true);
          }
          active_context.raster = ee.Image.loadGeoTIFF(datasets[key]);

          var mean_reducer = ee.Reducer.percentile([10, 90], ['p10', 'p90']);
          var meanDictionary = active_context.raster.reduceRegion({
            reducer: mean_reducer,
            geometry: active_context.map.getBounds(true),
            bestEffort: true,
          });

          ee.data.computeValue(meanDictionary, function (val) {
            active_context.visParams = {
              min: val['B0_p10'],
              max: val['B0_p90'],
              palette: active_context.visParams.palette,
            };
            active_context.last_layer = active_context.map.addLayer(
              active_context.raster, active_context.visParams);
            min_val.setValue(active_context.visParams.min, false);
            max_val.setValue(active_context.visParams.max, false);
            min_val.setDisabled(false);
            max_val.setDisabled(false);
            self.setValue(original_value, false);
            self.setDisabled(false);
          });
      }
    });


    var min_val = ui.Textbox(
      0, 0, function (value) {
        active_context.visParams.min = +(value);
        updateVisParams();
      });
    min_val.setDisabled(true);

    var max_val = ui.Textbox(
      100, 100, function (value) {
        active_context.visParams.max = +(value);
        updateVisParams();
      });
    max_val.setDisabled(true);

    active_context.point_val = ui.Textbox('nothing clicked');
    function updateVisParams() {
      if (active_context.last_layer !== null) {
        active_context.last_layer.setVisParams(active_context.visParams);
      }
    }
    active_context.updateVisParams = updateVisParams;
    select.setPlaceholder('Choose a dataset...');
    var range_button = ui.Button(
      'Detect Range', function (self) {
        self.setDisabled(true);
        var base_label = self.getLabel();
        self.setLabel('Detecting...');
        var mean_reducer = ee.Reducer.percentile([10, 90], ['p10', 'p90']);
        var meanDictionary = active_context.raster.reduceRegion({
          reducer: mean_reducer,
          geometry: active_context.map.getBounds(true),
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
    panel.add(active_context.point_val);
    panel_list.push([panel, min_val, max_val, active_context]);
    active_context.map.add(panel);

    function build_legend_panel() {
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

      function changeColorScheme(key) {

      };

      var names = ['Low', '', '', '', 'High'];
      legend_panel.add(legend_select);

      // Add color and and names
      for (var i = 0; i<5; i++) {
        legend_panel.add(makeRow(active_context.visParams.palette[i], names[i]));
      }
      if (active_context.legend_panel !== null) {
        active_context.remove(active_context.legend_panel);
      }
      active_context.legend_panel = active_context.map.add(legend_panel);
    };

    active_context.map.setControlVisibility(false);
    active_context.map.setControlVisibility({"mapTypeControl": true});
    build_legend_panel();
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

//panel_list.push([panel, min_val, max_val, map, active_context]);
panel_list.forEach(function (panel_array) {
  var map = panel_array[3].map;
  map.onClick(function (obj) {
    var point = ee.Geometry.Point([obj.lon, obj.lat]);
    [panel_list[0][3], panel_list[1][3]].forEach(function (active_context) {
      if (active_context.last_layer !== null) {
        active_context.point_val.setValue('sampling...')
        var point_sample = active_context.raster.sampleRegions({
          collection: point,
          //scale: 10,
          //geometries: true
        });
        ee.data.computeValue(point_sample, function (val) {
          if (val.features.length > 0) {
            active_context.point_val.setValue(val.features[0].properties.B0.toString());
            if (active_context.last_point_layer !== null) {
              active_context.map.remove(active_context.last_point_layer);
            }
            active_context.last_point_layer = active_context.map.addLayer(
              point, {'color': '#FF00FF'});
          } else {
            active_context.point_val.setValue('nodata');
          }
        });
      }
    });
  });
});

panel_list[0][0].add(clone_to_right);
panel_list[1][0].add(clone_to_left);
