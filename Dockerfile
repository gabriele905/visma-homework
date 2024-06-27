FROM python:3.9-slim-buster

WORKDIR /usr/src

COPY requirements.txt .

RUN set -ex \
    && python3.9 -m venv /venv \
    && /venv/bin/pip install -U pip \
    && LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "/venv/bin/pip install --no-cache-dir -r requirements.txt"

COPY . .
