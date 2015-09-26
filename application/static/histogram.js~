var jsonValue = json
$(function () {
    $('#rate').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Currency arbitrage'
        },
        subtitle: {
            text: 'Comparison of the final rates'
        },

        yAxis: {
            min: 0,
            title: {
                text: 'Rate (USD)'
            }
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        animation : true,
        series: [{
            name: 'Bellman-Ford',
            data: [jsonValue.bf.totalRate]

        }, {
            name: 'Genetic Algorithm',
            data: [1]

        }, {
            name: 'Recuit',
            data: [1]

        }]
    });
});


var jsonValue = json
$(function () {
    $('#time').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Currency arbitrage'
        },
        subtitle: {
            text: 'Comparison of the time taken'
        },

        yAxis: {
            min: 0,
            title: {
                text: 'time'
            }
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        animation : true,
        series: [{
            name: 'Bellman-Ford',
            data: [jsonValue.bf.timer]

        }, {
            name: 'Genetic Algorithm',
            data: [0.0001]

        }, {
            name: 'Recuit',
            data: [0.0001]

        }]
    });
});
