import pandas as pd
import urllib
import urllib.request
import json
from dbmodule import dbModule, conn

oracle_db = dbModule.Database()
conn = conn.conn()
# 대산읍(당진) x: 51 y:113
# 일산동(울산) x: 104 y:83

ServiceKey = "eTQfDTfcoqpr+U5Shz2IeDH0NIT3W2dtq/MWCu9gMP+LjUL3nIYXFujSkR22lCxaXAeQqyuYjfvkVFxG3oewfQ=="
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst'

# will be executing for every 00:00:00 AM as a batch program.
def get_tomorrow_forecast(location, today_date, tomorrow_date):
    if location == 'dangjin':
        nx = 51
        ny = 113
    elif location == 'ulsan':
        nx = 104
        ny = 83

    today_date = today_date.replace('-', '')

    queryParams = '?' + urllib.parse.urlencode(
        {
            urllib.parse.quote_plus('ServiceKey'): ServiceKey,  # key를 바로 입력해도 됩니다.
            # 총 14개의 항목을 3시간 단위로 순차적으로 불러옵니다. 다음날 24시간예보에 필요한 만큼만 가져왔습니다.
            urllib.parse.quote_plus('numOfRows'): '113',
            # JSON, XML 두가지 포멧을 제공합니다.
            urllib.parse.quote_plus('dataType'): 'JSON',
            # base_date --> 현재 날짜
            # 예보 받을 날짜를 입력합니다. 최근 1일간의 자료만 제공합니다.
            urllib.parse.quote_plus('base_date'): today_date, #20210607
            # 예보 시간을 입력합니다. 2시부터 시작하여 3시간 단위로 입력 가능합니다.
            urllib.parse.quote_plus('base_time'): '1400',
            # 울산 태양광 발전소 x 좌표입니다. '기상청18_동네예보 조회서비스_오픈API활용가이드.zip'에 포함 된 excel파일을 통해 확인 가능합니다.
            urllib.parse.quote_plus('nx'): nx,
            # 울산 태양광 발전소 y 좌표입니다. '기상청18_동네예보 조회서비스_오픈API활용가이드.zip'에 포함 된 excel파일을 통해 확인 가능합니다.
            urllib.parse.quote_plus('ny'): ny
        }
    )

    response = urllib.request.urlopen(url + queryParams).read()
    response = json.loads(response)
    # print("weatherAPI.py -- response:", response)

    fcst_df = pd.DataFrame()
    # fcst_df['Forecast_time'] = [f'{date} {hour}:00' for hour in range(24)]
    fcst_df['forecasttime'] = [tomorrow_date+' '+'%02d'%hour+':00:00' for hour in range(24)]
    row_idx = 0

    for i, data in enumerate(response['response']['body']['items']['item']):
        if i > 19:
            if data['category']=='REH':
                fcst_df.loc[row_idx, 'humidity'] = float(data['fcstValue'])
                # print('category:Humidity,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
            elif data['category']=='T3H':
                fcst_df.loc[row_idx, 'temperature'] = float(data['fcstValue'])
                # print('category:Temperature,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
            elif data['category']=='SKY':
                fcst_df.loc[row_idx, 'cloud'] = float(data['fcstValue'])
                # print('category:Cloud,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
            elif data['category']=='VEC':
                fcst_df.loc[row_idx, 'winddirection'] = float(data['fcstValue'])
                # print('category:WindDirection,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
            elif data['category']=='WSD':
                fcst_df.loc[row_idx, 'windspeed'] = float(data['fcstValue'])
                # print('category:WindSpeed,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'], '\n')
                row_idx+=3
    fcst_df = fcst_df.iloc[:24]
    fcst_df['forecasttime'] = pd.to_datetime(fcst_df['forecasttime'])
    fcst_df.interpolate(method='linear', inplace=True, limit_direction='both')

    # check first if there was an already a same forecast.
    # if there is, replace it with the latest forecast.
    # if none, append directly

    # check_table_existency_sql = "SELECT COUNT(*) FROM USER_TABLES WHERE TABLE_NAME = UPPER(\'{}\')".format(location+"_forecast_by_api")
    # table_existency = pd.read_sql(check_table_existency_sql, conn)
    # # print("table_existency:", table_existency)
    #
    # if table_existency.values[0] == 1:
    #     for i in range(len(fcst_df)):
    #             check_for_same_sql = "delete from {}_forecast_by_api where forecasttime = TO_DATE(\'{}\')".format(location, fcst_df["forecasttime"][i])
    #             sqlquery = sql.expression.text(check_for_same_sql)
    #             conn.execute(sqlquery)
    #             # print("deleted!")
    # else:
    #     pass
    #
    # # save the dataframe to Database.
    # fcst_df.to_sql(name=location+'_forecast_by_api', con=conn, if_exists='append', index=False,
    # dtype={
    #     'forecasttime':sqlalchemy.DateTime(),
    #     'humidity':sqlalchemy.types.Float(),
    #     'cloud':sqlalchemy.types.Float(),
    #     'temperature':sqlalchemy.types.Float(),
    #     'winddirection':sqlalchemy.types.Float(),
    #     'windspeed':sqlalchemy.types.Float()
    # })

    return fcst_df

# test
# dangjin_fcst_df = get_tomorrow_forecast('dangjin', '2021-06-07', '2021-06-08')
# ulsan_fcst_df = get_tomorrow_forecast('ulsan', '2021-06-07', '2021-06-08')