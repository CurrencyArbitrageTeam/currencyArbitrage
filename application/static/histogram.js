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
              else{
                return '<b> Oops an error occured </b>';
              }

            }
        },

        animation : true,
        series: [{
            name: 'BellmanFord',
              data: [jsonValue.BellmanFord.totalRate]

        }, {
            name: 'Genetic Algorithm',
            data: [1]

        }, {
            name: 'Annealing',
            data: [jsonValue.Annealing.totalRate]

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
              else{
                return '<b> Oops an error occured </b>';
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
            data: [0.0001]

        }, {
            name: 'Annealing',
            data: [jsonValue.Annealing.timer]

        }]
    });
});
