from flask import Flask, render_template, redirect, url_for, request, jsonify, make_response
import pandas as pd


# 랜덤 값 받기
from time import time
from random import random
import json

#이거는 flask 웹입니다.
app = Flask(__name__)

@app.route("/")
def index():
    data = pd.read_csv(".csv")
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
