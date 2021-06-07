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

    def get_dangjin(self, start, end, column, change=0):
        if '온도' in column:
            column = 'temperature'
        elif '습도' in column:
            column = 'humidity'
        elif '일조' in column:
            column = 'sunshinehour'
        else:
            column = 'cloud'
            change = 1
        # print(column)
        sql = """select fc.timedate, NVL(obs.{2}, {3}) , fc.{2}
                    from dangjin_obs obs right outer join dangjin_fcst fc on obs.timedate = fc.timedate
                    where fc.timedate between '{0}' AND '{1}'
                    order by fc.timedate""".format(start, end, column, change)
        data = pd.read_sql(sql, conn)
        return data


    def get_ulsan(self, start, end, column, change=0):
        if '온도' in column:
            column = 'temperature'
        elif '습도' in column:
            column = 'humidity'
        elif '일조' in column:
            column = 'sunshinehour'
        else:
            column = 'cloud'
            change = 1
        sql = """select fc.timedate, NVL(obs.{2}, {3}) , fc.{2}
                        from ulsan_obs obs right outer join ulsan_fcst fc on obs.timedate = fc.timedate
                        where fc.timedate between '{0}' AND '{1}'
                        order by fc.timedate""".format(start, end, column, change)
        data = pd.read_sql(sql, conn)
        return data
    def get_dangjin_energy(self, start, end, location):
        if '당진수상 태양광' in location:
            location = 'dangjin_floating'
        elif '당진자재창고태양광' in location:
            location = 'dangjin_warehouse'
        elif '당진태양광' in location:
            location = 'dangjin'
        sql = """select fc.timedate, NVL(obs.{2}, 0) , fc.{2}
                        from energy_obs obs right outer join energy_fcst fc on obs.timedate = fc.timedate
                        where fc.timedate between '{0}' AND '{1}'
                        order by fc.timedate""".format(start, end, location)
        data = pd.read_sql(sql, conn)
        return data


    def get_ulsan_energy(self, start, end, location):
        if '울산태양광' in location:
            location = 'ulsan'
        sql = """select fc.timedate, NVL(obs.{2},0) , fc.{2}
                        from energy_obs obs right outer  join energy_fcst fc on obs.timedate = fc.timedate
                        where fc.timedate between '{0}' AND '{1}'
                        order by fc.timedate""".format(start, end, location)

        data = pd.read_sql(sql, conn)
        return data
    
    def write_new_fcst(self, fcst_table_name, ):
        my_latest_date = pd.read_sql("select * from {} where 1=1 and timedate in select(max(timedate)")

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