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
    data = get_column_data("temperature", "dangjin_fcst")
    data = data["temperature"].values.tolist()

    return render_template("index.html", data=data)

@app.route("/map")
def Navermap():
    sql ="""select TO_CHAR(obs.timedate, 'YYYY')as year_,TO_CHAR(obs.timedate, 'MM') -1 as month_ , TO_CHAR(obs.timedate, 'DD')as day_ ,TO_CHAR(obs.timedate, 'HH24')as hour_,
                obs.cloud as temp_obs, fc.cloud as temp_fc
                from dangjin_obs obs join dangjin_fcst fc on obs.timedate = fc.timedate
                where obs.timedate between '2021-01-15' AND '2021-03-05'"""
    # sql = """select TO_CHAR(timedate, 'YYYY-MM-DD HH24:MI:SS')as year_, obs.cloud as temp_obs, fc.cloud as temp_fc
    #                 from dangjin_obs obs join dangjin_fcst fc on obs.timedate = fc.timedate
    #                 where obs.timedate between '2021-01-05' AND '2021-02-05'"""
    dangjin_obs = oracle_db.read_sql(sql)
    print(dangjin_obs)
    chart_data = []
    # date: new Date(2018, 0, i), open: open, close: close
    for row in dangjin_obs.itertuples():
        # print(row[1])
        chart_data.append(f"{{date:new Date( {row[1]}, {row[2]}, {row[3]}, {row[4]}), open: {row[5]}, close: {row[6]} }}")
    # print(','.join(chart_data))
    # print("--"*10)
    return render_template("view/map.html", data=','.join(chart_data) )

@app.route("/item_request", methods=['POST'])
def get_item():
    value1 = request.form['fromdate']
    value2 = request.form['todate']
    print("fromdate" + value1)
    print(value2)
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
    print(data)
    start = data['start']
    end = data['end']
    location = data['location']
    column = data['column']
    if '당진' in location:
        data = get_dangjin(start, end, column)
    elif '울산' in location:
        data = get_ulsan(start, end, column)

    # print(data)
    chart_data = []
    # date: new Date(2018, 0, i), open: open, close: close

    for row in data.itertuples():
        chart_data.append({"date":row[1].to_pydatetime(), "open":row[2], "close":row[3]})

    print("--" * 10)
    return jsonify(chart_data)

def get_dangjin(start, end, column):
    if '온도' in column:
        column = 'temperature'
    elif '습도' in column:
        column = 'humidity'
    elif '일조' in column:
        column = 'sunshinehour'
    else:
        column = 'cloud'
    print(column)
    sql = """select obs.timedate, obs.{2} , fc.{2}
                from dangjin_obs obs join dangjin_fcst fc on obs.timedate = fc.timedate
                where obs.timedate between '{0}' AND '{1}'""".format(start, end, column)
    data = oracle_db.read_sql(sql)
    return data


def get_ulsan(start, end, column):
    data = ""
    return data


if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
