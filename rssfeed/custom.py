import re

import requests
from bs4 import BeautifulSoup

from rssfeed.feed import Feed


class Dilbert(Feed):
    feed_url = "https://dilbert.com/feed"

    def transform_and_add(self, entry: dict) -> bool:
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
        return True


class Xkcd(Feed):
    feed_url = "https://xkcd.com/atom.xml"
    _re_id = re.compile(r"^https?://xkcd.com/(\d+)/?")

    def transform_and_add(self, entry: dict) -> bool:
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
        return True


class CommitStrip(Feed):
    feed_url = "https://www.commitstrip.com/en/feed/"

    def transform_and_add(self, entry: dict) -> bool:
        soup = BeautifulSoup(requests.get(entry["link"]).text, "html.parser")
        image = soup.find("div", attrs={"class": "entry-content"}).find("img")["src"]
        self.add_entry(
            title=entry["title"],
            updated=entry["updated"],
            link=entry["link"],
            image_link=image,
            mimetype="image/jpg",
        )
        return True


class Opraski(Feed):
    feed_url = "https://historje.tumblr.com/rss"

    def transform_and_add(self, entry: dict) -> bool:
        soup = BeautifulSoup(requests.get(entry["link"]).text, "html.parser")
        title = None
        for get_title in (
            lambda: soup.find("title").text.strip(),
            lambda: BeautifulSoup(entry["summary"]).text.strip(),
            lambda: entry["published"],
        ):
            try:
                title = get_title()
                break
            except Exception:
                continue
        if title is None:
            return False

        image = None
        for get_image in (
            lambda: soup.find("figure").find("img")["src"],
            lambda: soup.find("div", attrs={"class": "stat-media-wrapper"}).find("img")[
                "src"
            ],
            lambda: soup.find("meta", attrs={"property": "og:image:secure_url"})[
                "content"
            ],
        ):
            try:
                image = get_image()
                break
            except Exception:
                continue

        if image is None:
            return False

        self.add_entry(
            title=title,
            updated=entry["published"],
            link=entry["link"],
            content=None,
            image_link=image,
            mimetype=f"image/{image[-3:]}",
        )
        return True
