# version: 0.0.1
FROM python:3.6-alpine
MAINTAINER Xin Xiong <"xiongxin20008@126.com">
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
        ;
RUN mkdir /djcode
WORKDIR /djcode
ENV REFRESHED_AT 2018-12-27
ADD requirements.txt /djcode/
RUN pip install --no-cache-dir -r /djcode/requirements.txt
RUN rm -rf /root/.cache
RUN apk add --no-cache vim
EXPOSE 6001
