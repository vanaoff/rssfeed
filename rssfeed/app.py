from flask import Flask, Response

app = Flask(__name__)

CACHE = dict()


@app.route("/")
def hello():
    return "🚀🚀🚀"


@app.route("/dilbert")
def dilbert():
    from .dilbert import transform_feed

    xml = transform_feed(cache=CACHE)
    return Response(xml, mimetype="text/xml")
