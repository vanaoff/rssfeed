FROM python:slim

RUN pip install --no-cache gunicorn

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /rssfeed
RUN pip install /rssfeed

WORKDIR /var/rssfeed
ENTRYPOINT gunicorn --bind 0.0.0.0 "rssfeed:server()"
