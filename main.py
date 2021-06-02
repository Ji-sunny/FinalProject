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

@app.route("/")
def index():
    data = pd.read_csv("submission_0529.csv")
    return render_template("index.html", data=data)

@app.route("/map")
def Navermap():
    # sql = """select TO_CHAR(timedate, 'YYYY-MM-DD HH24:MI:SS')as timetime, cloud from ulsan_fcst
    #             where timedate <= '2021-9-10'
    #             order by timetime"""
    # md = oracle_db.read_sql(sql)
    # print(md)
    return render_template("view/map.html")

if __name__ == "__main__":
    app.debug = True
    app.run(port=8080)
