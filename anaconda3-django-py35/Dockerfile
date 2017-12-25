# Version: 0.0.1
FROM continuumio/anaconda3
MAINTAINER Xin Xiong "xiongxin20008@126.com"
RUN conda create -n django-py35 python=3.5
RUN source activate django-py35
COPY requirements.txt /use/src/app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uwsgi
EXPOSE 6001
