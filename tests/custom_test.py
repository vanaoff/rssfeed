import pytest

from rssfeed.custom import CommitStrip, Dilbert, ExistentialComics, Opraski, Xkcd


@pytest.mark.parametrize(
    "cls", (Opraski, CommitStrip, Xkcd, Dilbert, ExistentialComics)
)
def test_custom_feeds(cls):
    # Do not raise
    feed = cls.from_upstream()
    print(feed.to_string())
