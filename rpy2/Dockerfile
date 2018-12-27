FROM ubuntu:16.04

MAINTAINER Laurent Gautier <lgautier@gmail.com>, Belter <xiongxin20008@126.com>

ARG DEBIAN_FRONTEND=noninteractive
ARG CRAN_MIRROR=https://cloud.r-project.org

RUN \
apt-get update -qq && \
apt-get install -y \
apt-utils \
apt-transport-https \
dirmngr \
gnupg \
libcurl4-openssl-dev \
libnlopt-dev \
lsb-release
RUN \
echo "deb ${CRAN_MIRROR}/bin/linux/ubuntu $(lsb_release -c -s)/" \
>> /etc/apt/sources.list.d/added_repos.list && \
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9 && \
apt-get update -qq && \
apt-get install -y \
aptdaemon \
ed \
git \
mercurial \
libcairo-dev \
libedit-dev \
libxml2-dev \
python3 \
python3-pip \
python3.5-venv \
r-base \
r-base-dev \
sudo \
wget &&\
rm -rf /var/lib/apt/lists/*

RUN \
echo "broom\n\
DBI\n\
dbplyr\n\
dplyr\n\
hexbin\n\
ggplot2\n\
lme4\n\
RSQLite\n\
tidyr" > rpacks.txt && \
R -e 'install.packages(sub("(.+)\\\\n","\\1", scan("rpacks.txt", "character")), repos="'"${CRAN_MIRROR}"'")' && \
rm rpacks.txt

RUN \
python3 -m pip install --no-cache-dir --upgrade pip && \
python3 -m pip install --no-cache-dir --upgrade setuptools && \
python3 -m pip install --no-cache-dir --upgrade wheel && \
python3 -m pip install --no-cache-dir --upgrade numpy pandas sphinx jinja2 tzlocal && \
rm -rf /root/.cache
 
RUN \
python3 -m pip install --no-cache-dir \
https://bitbucket.org/rpy2/rpy2/get/version_2.9.x.tar.gz && \
rm -rf /root/.cache

RUN \
apt-get update -qq && \
apt-get install -y \
vim
