/**
 * request data from the Database.
 * data list should be...
 *      1. dangjin-weather
 *          1-1. Temperature
 *          1-2. Humidity
 *          1-3. Hr
 *          1-4. MJ/m2
 *          1-5. Cloud
 *          1-6. Time
 *      2. ulsan-weather
 *          2-1. Temperature
 *          2-2. Humidity
 *          2-3. Hr
 *          2-4. MJ/m2
 *          2-5. Cloud
 *          2-6. Time
 *      3. dangjin-energy
 *          3-1. location1
 *          3-2. location2
 *          3-3. location3
 *          3-4. location4
 *      4. ulsan-energy
 *          4-1. location1
 *          4-2. location2
 *          4-3. location3
 *          4-4. location4
 *
 */
am4core.ready(function() {

    am4core.useTheme(am4themes_animated);
    // Themes end

    var chart = am4core.create("xychart_1", am4charts.XYChart);
    chart.hiddenState.properties.opacity = 0; // this creates initial fade-in

    // request data

    var data = [];
    var open = 100;
    var close = 250;

    for (var i = 1; i < 120; i++) {
        open += Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 4);
        close = Math.round(open + Math.random() * 5 + i / 5 - (Math.random() < 0.5 ? 1 : -1) * Math.random() * 2);
        data.push({ date: new Date(2018, 0, i), open: open, close: close });
    }

    chart.data = data;

    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;

    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.dateX = "date";
    series.dataFields.openValueY = "open";
    series.dataFields.valueY = "close";
    series.tooltipText = "open: {openValueY.value} close: {valueY.value}";
    series.sequencedInterpolation = true;
    series.fillOpacity = 0.3;
    series.defaultState.transitionDuration = 1000;
    series.tensionX = 0.8;

    var series2 = chart.series.push(new am4charts.LineSeries());
    series2.dataFields.dateX = "date";
    series2.dataFields.valueY = "open";
    series2.sequencedInterpolation = true;
    series2.defaultState.transitionDuration = 1500;
    series2.stroke = chart.colors.getIndex(6);
    series2.tensionX = 0.8;

    chart.cursor = new am4charts.XYCursor();
    chart.cursor.xAxis = dateAxis;
    chart.scrollbarX = new am4core.Scrollbar();

}); // end am4core.ready()