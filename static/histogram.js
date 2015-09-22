$(function () {
    $('#container').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Comparison of the final rates'
        },
        subtitle: {
            text: 'DNF'
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
        animation : truee,
        series: [{
            name: 'Bellman-Ford',
            data: [49.9]

        }, {
            name: 'Genetic Algorithm',
            data: [83.6]

        }, {
            name: 'Recuit',
            data: [34.6]

        }]
    });
});
