FROM python:alpine

RUN pip install --no-cache gunicorn

COPY . /rssfeed
RUN pip install /rssfeed

CMD gunicorn --bind 0.0.0.0 rssfeed:app
