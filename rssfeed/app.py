import logging
import os
import time
from threading import Thread

from flask import Flask, Response, abort

from rssfeed.custom import Dilbert

logger = logging.getLogger(__name__)

FEEDS_DIR = "feeds"

FEEDS = ((Dilbert, "dilbert.xml"),)


def update_feeds(sleep=600):
    while True:
        for cls, filename in FEEDS:
            try:
                t0 = time.time()
                cls.from_upstream().to_file(os.path.join(FEEDS_DIR, filename))
                logger.info(
                    "%s RSS feed updated in %.2fs.", cls.__name__, time.time() - t0
                )
                time.sleep(sleep)
            except Exception:
                logger.error("%s RSS feed update failed", cls.__name__)


def server():
    logger.handlers = logging.getLogger("gunicorn.error").handlers
    logger.setLevel(logging.INFO)
    thread = Thread(target=update_feeds, args=())
    thread.daemon = True
    thread.start()

    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "🚀🚀🚀"

    @app.route("/<string:feed>")
    def feeds(feed):
        file = os.path.join(FEEDS_DIR, f"{feed}.xml")
        if os.path.exists(file):
            with open(file) as o:
                return Response(o.read(), mimetype="text/xml")
        else:
            abort(404, description="Resource not found 🤷‍♂️")

    return app
