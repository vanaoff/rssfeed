import re

import requests
from bs4 import BeautifulSoup

from rssfeed.feed import Feed


class Dilbert(Feed):
    feed_url = "https://dilbert.com/feed"

    def transform_and_add(self, entry: dict) -> None:
        soup = BeautifulSoup(requests.get(entry["link"]).text, "html.parser")
        head = soup.select("head")[0]
        extracted = dict()
        for key, property_ in [
            ("image", "og:image"),
            ("publish_date", "article:publish_date"),
            ("title", "og:title"),
        ]:
            extracted[key] = head.find("meta", property=property_)["content"].strip()
        self.add_entry(
            title=f"{extracted['publish_date']} - {extracted['title']}",
            updated=entry["updated"],
            link=entry["link"],
            image_link=extracted["image"],
        )


class Xkcd(Feed):
    feed_url = "https://xkcd.com/atom.xml"
    _re_id = re.compile(r"^https?://xkcd.com/(\d+)/?")

    def transform_and_add(self, entry: dict) -> None:
        soup = BeautifulSoup(entry["summary"], "html.parser")
        image = soup.find("img")
        number = self._re_id.search(entry["link"]).group(1)
        self.add_entry(
            title=f"Xkcd {number} - {entry['title']}",
            updated=entry["updated"],
            link=entry["link"],
            content=image["title"],
            image_link=image["src"],
            mimetype="image/png",
        )
