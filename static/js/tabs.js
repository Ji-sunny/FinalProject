<!-- 탭 부분 -->
$('#execute').click(function(){
    var time = $('#litepicker').val();
    start_date = time.substr(0, 10) + " 00:00:00"
    end_date = time.substr(13, 10) + " 23:00:00"
    var location = $('#check')[0].innerHTML;
    var column = document.getElementsByClassName("active")[0].innerText;
    var postdata = {'time':time, 'location':location, 'column':column}

    $.ajax({
        type: 'POST',
        url: '{{url_for("ajax")}}',
        data: JSON.stringify(postdata),
        dataType : 'JSON',
        contentType: "application/json",
        success: function(data){
            console.log("success")
            console.log(
                "time start_date:", start_date,
                "time end_date:", end_date
            )
            console.log("location:", location)
            console.log("column:", column)
        },
        error: function(request, status, error){
            console.log("failed")
            alert('ajax 통신 실패')
            alert(error);
        }
    })
})