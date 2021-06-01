from flask import Flask, render_template, redirect, url_for, request, jsonify

#이거는 flask 웹입니다.
app = Flask(__name__)


@app.route("/")
def index():
    result = "Hello"
    return render_template("index.html", data=result)

@app.route("/chart01")
def showchart01():
    return render_template("view/chart01.html")

@app.route("/chart02")
def showchart02():
    return render_template("view/chart02.html")

if __name__ == "__main__":
    app.debug = True
    app.run(port=8080)

