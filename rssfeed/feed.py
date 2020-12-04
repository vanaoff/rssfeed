import os
from abc import ABC, abstractmethod
from typing import List, Optional

import feedparser as fp
import requests
from feedgen.feed import FeedGenerator


class Feed(ABC):
    def __init__(
        self,
        id_: str,
        links: List[dict],
        title: str,
        updated: str,
    ):
        fg = FeedGenerator()
        fg.id(id_)
        fg.link(links)
        fg.title(title)
        fg.updated(updated)
        fg.generator("")
        self._feed_generator = fg

    @classmethod
    def from_xml(cls, feed_xml: str):
        parsed = fp.parse(feed_xml)
        head = parsed["feed"]
        entries = parsed["entries"]
        self = cls(head["id"], head["links"], head["title"], head["updated"])
        for entry in sorted(entries, key=lambda x: x["updated"], reverse=False):
            self.transform_and_add(entry)
        return self

    @classmethod
    def from_url(cls, feed_url: str):
        return cls.from_xml(requests.get(feed_url).text)

    @classmethod
    def from_upstream(cls):
        return cls.from_url(cls.feed_url)

    @property
    @abstractmethod
    def feed_url(self) -> str:
        pass

    def add_entry(
        self,
        title: str,
        link: str,
        updated: str,
        image_link: str,
        mimetype: str = "image/gif",
        content: Optional[str] = None,
    ) -> None:
        fe = self._feed_generator.add_entry()
        fe.id(link)
        fe.updated(updated)
        fe.title(title)
        fe.link([{"rel": "alternate", "type": mimetype, "href": image_link}])
        if content:
            fe.content(content)

    def transform_and_add(self, entry: dict) -> None:
        pass

    def to_string(self) -> str:
        return self._feed_generator.atom_str(pretty=True).decode("utf-8")

    def to_file(self, path: str) -> None:
        dirname, basename = os.path.split(path)
        os.makedirs(dirname, exist_ok=True)
        with open(path, "w") as w:
            w.write(self.to_string())
