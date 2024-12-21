FROM python:3.12.1-slim-bullseye


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app

RUN apt update -y && \
    apt install -y python3-dev gcc musl-dev && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY /app/* /app/

