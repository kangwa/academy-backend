FROM python:3

MAINTAINER Kangwa Bwali <kangwa2003@gmail.com>

ENV PYTHONUNBUFFERED 1

RUN mkdir /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
