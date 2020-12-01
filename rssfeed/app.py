from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello man ❤"


@app.route("/dilbert")
def dilbert():
    return "dilbert"


@app.route("/xkcd")
def xkcd():
    return "xkcd"


@app.route("/commit-strip")
def commit_strip():
    return "commit-strip"
