FROM mysql:8
<<<<<<< HEAD

COPY ./data.sql /docker-entrypoint-initdb.d/data.sql


=======
COPY ./data.sql /docker-entrypoint-initdb.d/data.sql

>>>>>>> e4ceb63 (- Setting up docker-compose file to create MySQL container)
# FROM python:latest
# ENV PYTHONUNBUFFERED 1
# RUN mkdir /Littlelemon
# WORKDIR /Littlelemon
# ADD ./requirements.txt /Littlelemon/
# RUN pip install -r requirements.txt
# ADD . /Littlelemon/