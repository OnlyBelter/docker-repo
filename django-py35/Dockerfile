# Version: 0.0.1
FROM python:3.5-alpine
MAINTAINER Xin Xiong "xiongxin20008@126.com"
ENV PYTHONUNBUFFERED 1
RUN set -e; \
	apk add --no-cache --virtual .build-deps \
		gcc \
		libc-dev \
		linux-headers \
                mariadb-dev \
                python3-dev \
                postgresql-dev \
                freetype-dev \
                libpng-dev \
                g++ \
                pcre \
                pcre-dev \
                tzdata  \
     	;
RUN mkdir /code
WORKDIR /code
ENV REFRESHED_AT 2017-12-25
ADD requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uwsgi
# ADD . /djcode/  # copy . to /djcode/
EXPOSE 6001
