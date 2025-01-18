FROM mysql:latest

COPY ./data.sql /docker-entrypoint-initdb.d/data.sql


# FROM python:latest
# ENV PYTHONUNBUFFERED 1
# RUN mkdir /ECommerce
# WORKDIR /ECommerce
# ADD ./requirements.txt /ECommerce/
# RUN pip install -r requirements.txt
# ADD . /ECommerce/