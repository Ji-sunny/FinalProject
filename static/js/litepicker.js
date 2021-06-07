var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

const picker = new Litepicker({
    element: document.getElementById('litepicker'),
    autoApply: true,
    singleMode: false,
    inlineMode: true, // 항상 열려있게
    lang: "ko-kr", // 언어 설정
    maxDays: 365, // 최대 선택 일자 수
    // scrollToDate: true,
    // showTooltip: true,
    // autoRefresh: true,
    setup: (picker) => {
        picker.on('selected', (date1, date2) => {
            date_1 = date1.dateInstance.toString().substr(4,21)
            date_2 = date2.dateInstance.toString().substr(4,21)
            var d1s = date_1.split(' ')
            var d2s = date_2.split(' ')
            d1s_m = d1s[0]
            d2s_m = d2s[0]
            var step;
            for (step = 0; step < 12; step++) {
                if (months[step] == d1s_m) {
                    d1s_m = (step+1)
                }
                if (months[step] == d2s_m) {
                    d2s_m = (step+1)
                }
            }
            if (d1s_m<10) {
                d1s_m = "0" + d1s_m.toString()
            }
            if (d2s_m<10) {
                d2s_m = "0" + d2s_m.toString()
            }

            console.log(d1s[2] + '-' + d1s_m + '-' + d1s[1] + " 00:00:00")
            console.log(d2s[2] + '-' + d2s_m + '-' + d2s[1] + " 23:00:00")

            start_date = d1s[2] + '-' + d1s_m + '-' + d1s[1] + " 00:00:00"
            end_date = d2s[2] + '-' + d2s_m + '-' + d2s[1] + " 23:00:00"


            $("#execute").trigger("click")

        })
        picker.on('error:data', () => {
            alert("선택불가능.")
        })
    }
});