from weatherAPI import get_tomorrow_forecast
from datetime import datetime, timedelta
import pandas as pd
from dbmodule import conn
import sqlalchemy
from sqlalchemy import sql
from tensorflow.keras.models import load_model
# 대산읍(당진) x: 51 y:113
# 일산동(울산) x: 104 y:83
conn = conn.conn()

# weather prediction with 2 additional sunshinehour, isolation columns.
# these predicted data will be used for predicting tomorrow's energy
def tomorrows_weather_with_sunshine_iso(location):
    today = datetime.now()
    today_date = today.strftime("%Y-%m-%d")
    tomorrow = today + timedelta(days=1)
    tomorrow_date = tomorrow.strftime("%Y-%m-%d")

    yesterday = today + timedelta(days=-1)
    yesterday_date = yesterday.strftime("%Y-%m-%d")

    if today.hour >= 14:
        # run after 14:00:00 AM
        fcst_df = get_tomorrow_forecast(location=location, today_date=today_date, tomorrow_date=tomorrow_date)
    else:
        # run on test if there's no tomorrow's forecast
        fcst_df = get_tomorrow_forecast(location=location, today_date=yesterday_date, tomorrow_date=today_date)

    fcst_df = rename_obs_df(fcst_df)
    fcst_df = round_obs_df(fcst_df)
    fcst_df = time_obs_df(fcst_df)
    test_sun = fcst_df.loc[:, ['temperature', 'humidity', 'cloud', 'month', 'day', 'hour']]

    dangjin_sun_model = load_model('./model/sunshine/dangjin_sun.hdf5')
    pred_sunshin_dangjin = dangjin_sun_model.predict(test_sun)
    fcst_df["sunshinehour"] = pred_sunshin_dangjin
    test_iso = fcst_df.loc[:,['temperature', 'humidity', 'windspeed', 'winddirection', 'cloud', 'month', 'day', 'hour']]

    dangjin_iso_model = load_model('./model/isolation/dangjin_model_iso.hdf5')
    pred_iso_dangjin = dangjin_iso_model.predict(test_iso)
    fcst_df["isolation"] = pred_iso_dangjin

    # check first if there was an already a same forecast.
    # if there is, replace it with the latest forecast.
    # if none, append directly
    check_table_existency_sql = "SELECT COUNT(*) FROM USER_TABLES WHERE TABLE_NAME = UPPER(\'{}\')".format(location + "_prediction")
    table_existency = pd.read_sql(check_table_existency_sql, conn)
    # print("table_existency:", table_existency)

    if table_existency.values[0] == 1:
        for i in range(len(fcst_df)):
                check_for_same_sql = "delete from {}_prediction where time = TO_DATE(\'{}\')".format(location, fcst_df["time"][i])
                sqlquery = sql.expression.text(check_for_same_sql)
                conn.execute(sqlquery)
                # print("deleted!")
    else:
        pass
    fcst_df = reindex_fcst(fcst_df)
    fcst_df.to_sql(name=location + '_prediction', con=conn, if_exists='append', index=False,
                   dtype={
                       'time': sqlalchemy.DateTime(),
                       'humidity': sqlalchemy.types.Float(),
                       'cloud': sqlalchemy.types.Float(),
                       'temperature': sqlalchemy.types.Float(),
                       'winddirection': sqlalchemy.types.Float(),
                       'windspeed': sqlalchemy.types.Float(),
                       'month':sqlalchemy.types.Integer(),
                       'day': sqlalchemy.types.Integer(),
                       'hour': sqlalchemy.types.Integer(),
                   })

    print("task done.")


def rename_obs_df(df_):
    df = df_.copy()
    df = df.rename(columns={
        "forecasttime": "time",
        "temperature": "temperature"})
    return df

def round_obs_df(df_):
    df = df_.copy()
    df.loc[:,["temperature", "humidity", "windspeed", "winddirection", "cloud"]] = df.loc[:,["temperature", "humidity", "windspeed", "winddirection", "cloud"]].apply(lambda x: round(x,1))
    return df

def time_obs_df(df_):
    df = df_.copy()
    #     df['time'] = pd.to_datetime(df['time'])

    df['hour'] = df['time'].dt.hour
    df['month'] = df['time'].dt.month
    df['day'] = df['time'].dt.day
    df['year'] = df['time'].dt.year
    return df
def reindex_fcst(fcst_df):
    fcst_df = fcst_df.reindex(columns=["time", "temperature", "humidity", "windspeed", "winddirection", "cloud", "year", "month", "day", "hour", "sunshinehour", "isolation"])
    return fcst_df
# test
tomorrows_weather_with_sunshine_iso('dangjin')
tomorrows_weather_with_sunshine_iso('ulsan')