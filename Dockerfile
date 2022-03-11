FROM python:3.8.11-slim-buster
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

#COPY ./celery_conf/etc/init.d/celeryd /etc/init.d/celeryd
#COPY ./celery_conf/etc/default/celeryd /etc/default/celeryd

COPY . .
