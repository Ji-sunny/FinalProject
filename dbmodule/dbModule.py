from sqlalchemy import types, create_engine
import pandas as pd
from sqlalchemy.sql.expression import table
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
# ===============================IMDB===============================