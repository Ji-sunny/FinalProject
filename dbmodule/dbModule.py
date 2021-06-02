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
# ===============================IMDB===============================