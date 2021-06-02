$(function() {
    $('input[name="daterange"]').daterangepicker({
        opens: 'left',
    }, function(start, end, label) {
        console.log("dual_daterangepicker.js 콘솔 로그: " + start.format('YYYY-MM-DD 00:00:00') + ' to ' + end.format('YYYY-MM-DD 23:00:00'));
    });
});

//http://www.daterangepicker.com/ 참고!