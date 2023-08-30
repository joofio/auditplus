#FROM python:3.9-slim-buster
#FROM ubuntu:18.04
FROM python:3.10-slim
ARG GITHUB_SHA=dev
ARG MARIADB_USER= api
ARG MARIADB_PASSWORD=ZSCO1wtnkwU9fBsa5/fS
ARG MARIADB_HOST=127.0.0.1
ARG MARIADB_PORT=3306
ARG MARIADB_DB=repository

RUN echo $MARIADB_USER
RUN echo $MARIADB_PASSWORD
RUN echo $MARIADB_HOST
RUN echo $MARIADB_DB
RUN echo $MARIADB_PORT
RUN echo $GITHUB_SHA

ENV MARIADB_USER=$MARIADB_USER
ENV MARIADB_PASSWORD=$MARIADB_PASSWORD
ENV MARIADB_HOST=$MARIADB_HOST
ENV MARIADB_PORT=$MARIADB_PORT
ENV MARIADB_DB=$MARIADB_DB
ENV GITHUB_SHA=$GITHUB_SHA

RUN echo $MARIADB_USER
RUN echo $MARIADB_PASSWORD
RUN echo $MARIADB_HOST
RUN echo $MARIADB_DB
RUN echo $MARIADB_PORT


RUN mkdir /app
RUN mkdir /app/flaskapp
COPY flaskapp /app/flaskapp

COPY requirements.txt /app
COPY run.py /app
COPY gunicorn.sh /app
COPY init.sql /app
COPY *.zip /app

COPY *.sav /app

RUN apt-get update -y
#RUN apt-get install -y libmariadb-dev
#RUN apt-get install -y gcc

WORKDIR /app
RUN pip install -r requirements.txt
RUN unzip model.zip 

EXPOSE 5000
#CMD python run.py
RUN ["chmod", "+x", "./gunicorn.sh"]

ENTRYPOINT ["./gunicorn.sh"]
