FROM python:3.10-slim-bullseye

WORKDIR /app
RUN apt-get update

COPY . .

RUN pip install -r requirements.txt
