import pandas as pd
from dbmodule import conn

conn = conn.conn()


class Database():
    def __init__(self):
        self.pd = pd
    # ===========================================================================
    def read_data(self, tablesName):
        sql = "select * from {}".format(tablesName)
        data = pd.read_sql(sql, conn)
        # data 열이름 소문자처리
        data.columns = data.columns.str.lower()
        return data

    def read_data_all(self, table_name):
        data = self.pd.read_sql_table(table_name.lower(), conn)
        return data

    def read_sql(self, sql):
        data = pd.read_sql(sql, conn)
        return data

    def read_data_column(self, columnsName, tablesName):
        sql = "select {} from {}".format(columnsName, tablesName)
        data = pd.read_sql(sql, conn)
        # data 열이름 소문자처리
        data.columns = data.columns.str.lower()
        return data

    def read_data_column_by_time(self, columnsName, tablesName, start_time, end_time):
        sql = """
        select 
            TO_CHAR(obs.timedate, 'YYYY-MM-DD')as timetime, 
            obs.temperature as temp_obs, fc.temperature as temp_fc
        from dangjin_obs obs join dangjin_fcst fc on obs.timedate = fc.timedate
        where obs.timedate between start_time AND end_time;""".format(start_time, end_time)
        # sql = "select {} from {}".format(columnsName, tablesName)
        data = pd.read_sql(sql, conn)
        # data 열이름 소문자처리
        data.columns = data.columns.str.lower()
        return data
# ===============================weather===============================

class Weather:
    def __init__(self, timetime, temperature, humidity, sunshinehour, cloud):
        self.timetime = timetime
        self.temperature = temperature
        self.humidity = humidity
        self.sunshinehour = sunshinehour
        self.cloud = cloud

    def __str__(self):
        return f"{self.timetime}, {self.temperature}, {self.humidity}, " \
               f"{self.sunshinehour}, {self.cloud}"

    def to_dict(self):
        return {"timetime": self.timetime,
                "temperature": self.temperature,
                "humidity": self.humidity,
                "sunshinehour": self.sunshinehour,
                "cloud": self.cloud}