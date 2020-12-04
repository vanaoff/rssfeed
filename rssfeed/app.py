import logging
import os
import time
from threading import Thread
from typing import Type

from flask import Flask, Response, abort

from rssfeed.custom import Dilbert, Xkcd
from rssfeed.feed import Feed

logger = logging.getLogger(__name__)

FEEDS = {
    "dilbert": Dilbert,
    "xkcd": Xkcd,
}


def feed_file(name: str) -> str:
    return os.path.join("feeds", f"{name}.xml")


def read_feed(name: str) -> Response:
    with open(feed_file(name)) as o:
        return Response(o.read(), mimetype="text/xml")


def sync_feed(name: str, cls: Type[Feed], sleep: int = 600):
    while True:
        try:
            t0 = time.time()
            cls.from_upstream().to_file(feed_file(name))
            logger.info(
                "%s RSS feed updated in %.2fs.",
                name.capitalize(),
                time.time() - t0,
            )
            time.sleep(sleep)
        except Exception:
            logger.error("%s RSS feed update failed.", name.capitalize())


def server(timeout=120):
    gunicorn_logger = logging.getLogger("gunicorn.error")
    logger.handlers = gunicorn_logger.handlers
    logger.setLevel(gunicorn_logger.level)
    for name, cls in FEEDS.items():
        thread = Thread(target=sync_feed, args=(name, cls))
        thread.daemon = True
        thread.start()

    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "🚀🚀🚀"

    @app.route("/<string:feed>")
    def feeds(feed):
        if feed in FEEDS:
            for _ in range(timeout):
                try:
                    return read_feed(feed)
                except FileNotFoundError:
                    logger.debug("Feed %s not exists. Waiting 1s.", feed.capitalize())
                    time.sleep(1)
            else:
                abort(404, description="Not able to load feed 💥.")
        else:
            abort(404, description="Feed not supported 🤷‍♂️.")

    return app
