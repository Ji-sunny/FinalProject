from flask import Flask, render_template, redirect, url_for, request, jsonify, make_response
import pandas as pd
from flask_cors import CORS
from dbmodule import dbModule

oracle_db = dbModule.Database()

app = Flask(__name__)
cors = CORS(app)
# 랜덤 값 받기
from time import time
from random import random
import json

#이거는 flask 웹입니다.
app = Flask(__name__)

def get_column_data(column, table):
    data = oracle_db.read_data_column(column, table)
    return data

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/ajax', methods=['POST'])
def ajax():
    # if request.method == 'GET':
    #     if '당진' in location:
    #         dangjin_column_data = oracle_db.read_data_column_by_time(column, 'dangjin_fcst', time)
    #     return render_template("index.html", column_data=dangjin_column_data)
    # 미완성
    # elif request.method == 'POST':
    #     data = request.get_json()
    #     print(data)
    #
    #     return jsonify(result = "success", result2= data)
    data = request.get_json()
    start = data['start']
    end = data['end']
    location = data['location']
    column = data['column']
    if '당진' in location:
        data = get_dangjin(start, end, column)
        energy_data = get_dangjin_energy(start, end, location)
    elif '울산' in location:
        data = get_ulsan(start, end, column)
        energy_data = get_ulsan_energy(start, end, location)

    chart_data = []
    energy_chart_data = []
    # date: new Date(2018, 0, i), open: open, close: close
    # print(data)
    for row in data.itertuples():
        chart_data.append({"date":row[1].to_pydatetime(), "open":row[2], "close":row[3]})
    for row in energy_data.itertuples():
        energy_chart_data.append({"date":row[1].to_pydatetime(), "open":row[2], "close":row[3]})
    # print("--" * 10)
    return jsonify({"chart_data":chart_data, "energy_chart_data":energy_chart_data})

def get_dangjin(start, end, column, change=0):
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
    data = oracle_db.read_sql(sql)
    return data


def get_ulsan(start, end, column, change=0):
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
    data = oracle_db.read_sql(sql)
    return data
def get_dangjin_energy(start, end, location):
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
    energy_data = oracle_db.read_sql(sql)
    return energy_data


def get_ulsan_energy(start, end, location):
    if '울산태양광' in location:
        location = 'ulsan'
    sql = """select fc.timedate, NVL(obs.{2},0) , fc.{2}
                    from energy_obs obs right outer  join energy_fcst fc on obs.timedate = fc.timedate
                    where fc.timedate between '{0}' AND '{1}'
                    order by fc.timedate""".format(start, end, location)

    energy_data = oracle_db.read_sql(sql)
    return energy_data


if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
