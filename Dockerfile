FROM python:3.10

RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080