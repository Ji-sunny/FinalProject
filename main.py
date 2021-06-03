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
    # sql = """select TO_CHAR(timedate, 'YYYY-MM-DD HH24:MI:SS')as timetime, cloud from ulsan_fcst
    #             where timedate <= '2021-9-10'
    #             order by timetime"""
    # md = oracle_db.read_sql(sql)
    # print(md)
    return render_template("view/map.html")

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
    return jsonify(result = "success", result2= data)

if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
