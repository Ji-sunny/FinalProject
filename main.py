from flask import Flask, render_template, redirect, url_for, request, jsonify, make_response
import pandas as pd
from flask_cors import CORS
from dbmodule import dbModule

oracle_db = dbModule.Database()

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/ajax', methods=['POST'])
def ajax():
    data = request.get_json()
    start = data['start']
    end = data['end']
    location = data['location']
    column = data['column']

    energy_sum_data = oracle_db.get_energy_sum(start, end, location)

    if '당진' in location:
        data = oracle_db.get_dangjin(start, end, column)
        energy_data = oracle_db.get_dangjin_energy(start, end, location)

    elif '울산' in location:
        data = oracle_db.get_ulsan(start, end, column)
        energy_data = oracle_db.get_ulsan_energy(start, end, location)

    barchart_data = []
    chart_data = []
    energy_chart_data = []
    # date: new Date(2018, 0, i), open: open, close: close
    # print(data)
    for row in data.itertuples():
        chart_data.append({"date":row[1].to_pydatetime(), "open":row[2], "close":row[3]})
    for row in energy_data.itertuples():
        energy_chart_data.append({"date":row[1].to_pydatetime(), "open":row[2], "close":row[3]})
    for row in energy_sum_data.itertuples():
        barchart_data.append({"date":row[1], "steps":row[2]})

    # print("--" * 10)
    return jsonify({"chart_data":chart_data, "energy_chart_data":energy_chart_data, "barchart_data":barchart_data})

@app.route("/select")
def selectmain():
    return render_template('view/select.html')

if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)