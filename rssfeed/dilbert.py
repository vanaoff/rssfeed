from typing import Optional

import feedparser as fp
import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

FEED_URL = "https://dilbert.com/feed"


def transform_feed(cache: Optional[dict] = None):
    cache = cache or dict()
    parsed = fp.parse(requests.get(FEED_URL).text)
    feed = parsed["feed"]
    entries = parsed["entries"]
    fg = FeedGenerator()
    fg.id(feed["id"])
    fg.link(feed["links"])
    fg.title(feed["title"])
    fg.updated(feed["updated"])
    fg.generator("")

    for entry in sorted(entries, key=lambda x: x["updated"], reverse=False):
        fe = fg.add_entry()
        item_id = entry["link"]
        fe.id(item_id)
        fe.updated(entry["updated"])

        if item_id not in cache:
            cache[item_id] = item_cache = dict()
            soup = BeautifulSoup(requests.get(entry["link"]).text, "html.parser")
            head = soup.select("head")[0]
            for key, property_ in [
                ("image", "og:image"),
                ("publish_date", "article:publish_date"),
                ("title", "og:title"),
            ]:
                item_cache[key] = head.find("meta", property=property_)[
                    "content"
                ].strip()
        else:
            item_cache = cache
        fe.title(f"{item_cache['publish_date']} - {item_cache['title']}")
        fe.link(
            [{"rel": "alternate", "type": "image/gif", "href": item_cache["image"]}]
        )
    return fg.atom_str(pretty=True).decode("utf-8")
