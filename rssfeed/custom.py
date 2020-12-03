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
            title=extracted["title"],
            publish_date=extracted["publish_date"],
            updated=entry["updated"],
            link=entry["link"],
            image_link=extracted["image"],
        )
