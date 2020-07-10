FROM python:3.8.3-alpine

RUN mkdir -p /home/app
ENV HOME=/home/app
ENV APP_HOME=/home/app/frontend
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add jpeg-dev zlib-dev libjpeg

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .

COPY . .

RUN flake8 --ignore=E501,F401 .

ENTRYPOINT ["sh", "/home/app/frontend/entrypoint.sh"]
