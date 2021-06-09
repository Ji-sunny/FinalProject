import numpy as np
import pandas as pd
from datetime import datetime
from dbmodule import conn
import joblib
import sqlalchemy

conn = conn.conn()

def tomorrows_energy():
    today = datetime.now()
    today_date = today.strftime("%Y-%m-%d")
    location = ['dangjin', 'dangjin_floating', 'dangjin_warehouse', 'ulsan']

    # to collect location's energy by every column
    energy_df = pd.DataFrame(columns=location)
    timedate = pd.DataFrame(columns=['timedate'])
    for loc in location:
        # predicted_df
        if 'dangjin' in loc:
            sql = "select * from {}_prediction where \'{}\'<=time".format('dangjin', today_date)
            fcst_df = pd.read_sql(sql , conn)
        elif 'ulsan' in loc:
            sql = "select * from {}_prediction where \'{}\'<=time".format('ulsan', today_date)
            fcst_df = pd.read_sql(sql , conn)
        # 해의 유무
        fcst_df["solar"] = fcst_df["sunshinehour"].map(lambda x: 0 if x == 0 else 1)

        # 전운량 정규화
        fcst_df["cloud_norm"] = fcst_df["cloud"].map(lambda x: x / 10)

        n = 0
        fcst_df["temp_day_max"] = np.nan
        while True:
            fcst_df.loc[24 * n:24 * (n + 1), "temp_day_max"] = fcst_df.loc[24 * n:24 * (n + 1), "temperature"].max()
            fcst_df.loc[24 * n:24 * (n + 1), "temp_day_min"] = fcst_df.loc[24 * n:24 * (n + 1), "temperature"].min()
            mean = fcst_df.loc[24 * n:24 * (n + 1), "temperature"].mean()
            fcst_df.loc[24 * n:24 * (n + 1), "temp_day_mean"] = round(mean, 2)

            fcst_df.loc[24 * n:24 * (n + 1), "hum_day_max"] = fcst_df.loc[24 * n:24 * (n + 1), "humidity"].max()
            fcst_df.loc[24 * n:24 * (n + 1), "hum_day_min"] = fcst_df.loc[24 * n:24 * (n + 1), "humidity"].min()
            mean = fcst_df.loc[24 * n:24 * (n + 1), "humidity"].mean()
            fcst_df.loc[24 * n:24 * (n + 1), "hum_day_mean"] = round(mean, 2)
            fcst_df.loc[24 * n:24 * (n + 1), "sunshinehour_isolation"] = fcst_df.loc[24 * n:24 * (n + 1), "sunshinehour"] * fcst_df.loc[24 * n:24 * (n + 1), "isolation"]

            n += 1
            if 24 * n > len(fcst_df):
                break

            print("fcst_df.columns:", fcst_df.columns)

        # load model by location detail
        if loc == 'dangjin':
            model = joblib.load("model/lgbm/lgbm365_dangjin_model.pkl")
        elif loc == 'dangjin_floating':
            model = joblib.load("model/lgbm/lgbm365_dangjin_floating_model.pkl")
        elif loc == 'dangjin_warehouse':
            model = joblib.load("model/lgbm/lgbm365_dangjin_warehouse_model.pkl")
        elif loc == 'ulsan':
            model = joblib.load("model/lgbm/lgbm365_ulsan_model.pkl")

        Xs = ['hour', 'temperature', 'isolation', 'month', 'day', 'humidity',
              'winddirection', 'windspeed', 'sunshinehour', 'cloud', 'cloud_norm', 'sunshinehour_isolation']

        # predict energy by model
        # & stack up the predictions into energy_df
        energy_df[loc] = model.predict(fcst_df[Xs].to_numpy())

    timedate = fcst_df['time']
    energy_df = pd.concat([timedate, energy_df], axis=1)

    check_table_existency_sql = "SELECT COUNT(*) FROM USER_TABLES WHERE TABLE_NAME = UPPER(\'{}\')".format("energy_fcst_test")
    table_existency = pd.read_sql(check_table_existency_sql, conn)

    if table_existency.values[0] == 1:
        for i in range(len(fcst_df)):
                check_for_same_sql = "delete from energy_fcst_test where forecasttime = TO_DATE(\'{}\')".format(location, energy_df["time"][i])
                sqlquery = sql.expression.text(check_for_same_sql)
                conn.execute(sqlquery)
                # print("deleted!")
    else:
        pass

    # store predicted energy
    # energy_df.to_sql(name='energy_fcst_test', con=conn, if_exists='append', index=False,
    #                  dtype={
    #                      'timedate': sqlalchemy.DateTime(),
    #                      'dangjin_floating': sqlalchemy.types.Float(),
    #                      'dangjin_warehouse': sqlalchemy.types.Float(),
    #                      'dangjin': sqlalchemy.types.Float(),
    #                      'ulsan': sqlalchemy.types.Float()
    #                  })
    print(energy_df)
    return energy_df

    # 즉각 학습하는 내용도 추가?

tomorrows_energy()