var jsonValue = json
$(function () {
    $('#rate').highcharts({
        credits: {
        enabled: false
        },
        chart: {
            type: 'column'
        },
        title: {
            text: 'Final rates'
        },
        subtitle: {
            text: 'Comparison of the final rates'
        },

        yAxis: {
            min: 1,
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
        tooltip: {
            formatter: function () {
              if ( this.series.name == "BellmanFord"){
                return '<b>' + jsonValue.BellmanFord.way + '<br> <b>Rate : </b>' + this.point.y + '</b>';
              }
              if ( this.series.name == "Annealing"){
                return '<b>' + jsonValue.Annealing.way + ' <br> <b>Rate :</b> ' + this.point.y + '</b>';
              }
              if ( this.series.name == "GA_Annealing"){
                return '<b>' + jsonValue.GA_Annealing.way + ' <br> <b>Rate :</b> ' + this.point.y + '</b>';
              }
              else{
                return '<b>' + jsonValue.GA.way + ' <br> <b>Rate :</b> ' + this.point.y + '</b>';
              }

            }
        },

        animation : true,
        series: [{
            name: 'BellmanFord',
              data: [jsonValue.BellmanFord.totalRate]

        }, {
            name: 'Genetic Algorithm',
            data: [jsonValue.GA.totalRate]

        }, {
            name: 'Annealing',
            data: [jsonValue.Annealing.totalRate]

        }, {
            name: 'Genetic Algorithm + Annealing',
            data: [jsonValue.GA_Annealing.totalRate]

        }]
    });
});


var jsonValue = json
$(function () {
    $('#time').highcharts({
        credits: {
        enabled: false
        },
        chart: {
            type: 'column'
        },
        title: {
            text: 'Total time'
        },
        subtitle: {
            text: 'Comparison of the time taken'
        },

        yAxis: {
            type: 'logarithmic',
            title: {
                text: 'Time (sec)'
            }
        },
        tooltip: {
            formatter: function () {
              if ( this.series.name == "BellmanFord"){
                return '<b>' + jsonValue.BellmanFord.way + '</b><br><b>Time : </b>' + this.point.y + ' seconds';
              }
              if ( this.series.name == "Annealing"){
                return '<b>' + jsonValue.Annealing.way + '</b><br><b>Time : </b>' + this.point.y + ' seconds';
              }
              if ( this.series.name == "GA_Annealing"){
                return '<b>' + jsonValue.GA_Annealing.way + '</b><br><b>Time : </b>' + this.point.y + ' seconds';
              }
              else{
                return '<b>' + jsonValue.GA.way + ' <br> <b>Time :</b> ' + this.point.y + ' seconds';
              }

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
            name: 'BellmanFord',
            data: [jsonValue.BellmanFord.timer]

        }, {
            name: 'Genetic Algorithm',
            data: [jsonValue.GA.timer]

        }, {
            name: 'Annealing',
            data: [jsonValue.Annealing.timer]

        }, {
            name: 'Genetic Algorithm + Annealing',
            data: [jsonValue.GA_Annealing.timer]

        }]
    });
});

$(function () {

    $('#convergenceRate').highcharts({
        title: {
            text: 'Evolution of the population'
        },
        subtitle: {
            text: 'Genetic Algorithm'
        },
        xAxis: {
            tickInterval: 1,
            gridLineWidth: 1,
            title: {
                enabled: true,
                text: 'Iteration'
            },
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true
        },
        yAxis: {
            title: {
                text: 'Rate (USD)'
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        },
        series: [{
            name: 'Individual',
            type: 'scatter',
            color: Highcharts.getOptions().colors[1],
            data: jsonConvergenceRate

        }],
        tooltip: {
            headerFormat: '<b>{series.name}</b><br>',
            pointFormat: 'Itérations n° {point.x}, {point.y} USD'
        }
    });
});


$(function () {

    $('#convergenceCurrencies').highcharts({
        title: {
            text: 'Evolution of the population'
        },
        subtitle: {
            text: 'Genetic Algorithm'
        },
        xAxis: {
            tickInterval: 1,
            gridLineWidth: 1,
            title: {
                enabled: true,
                text: 'Iteration'
            },
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true
        },
        yAxis: {
            title: {
                text: 'Currencies Number'
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        },
        series: [{
            name: 'Individual',
            type: 'scatter',
            color: Highcharts.getOptions().colors[1],
            data: jsonConvergenceCurrencies

        }],
        tooltip: {
            headerFormat: '<b>{series.name}</b><br>',
            pointFormat: 'Itérations n° {point.x}, {point.y} currency number'
        }
    });
});
