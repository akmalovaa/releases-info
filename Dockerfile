FROM python:3.11.3-slim-buster

RUN apt update && apt upgrade -y && pip install poetry

WORKDIR /app

COPY . .

RUN poetry config virtualenvs.create false
RUN poetry install