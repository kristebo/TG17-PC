FROM debian:jessie
LABEL maintainer "adriah@ifi.uio.no"

RUN apt-get update && apt-get install -y python2.7 python-pip

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY src/ /usr/src/app

RUN pip install -r requirements.txt

EXPOSE 5000
