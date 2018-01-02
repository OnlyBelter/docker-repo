FROM rpy2/rpy2:2.9.x

MAINTAINER Laurent Gautier <lgautier@gmail.com>, Xin Xiong <xiongxin20008@126.com>

ARG DEBIAN_FRONTEND=noninteractive
ARG CRAN_MIRROR=https://cran.revolutionanalytics.com/

RUN \
  apt-get update -qq && \
  apt-get install -y \
                     software-properties-common\
                     python3-dev \
                     libssl-dev \
                     libcurl4-openssl-dev \
                     libxml2-dev

# install MariaDB
RUN \
  apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8  &&\
  add-apt-repository 'deb [arch=amd64,i386,ppc64el] http://mirrors.neusoft.edu.cn/mariadb/repo/10.2/ubuntu xenial main' &&\
  apt-get update -qq && \
  apt-get install -y \
                     mariadb-client \
                     libmariadbclient-dev
# install Java
RUN \
  apt-get install -y openjdk-8-jdk  && \
  rm -rf /var/lib/apt/lists/*  && \
  R CMD javareconf

ADD ./package/ /src/
RUN \
  cd /src && \
  R -e 'install.packages(sub("(.+)\\\\n","\\1", scan("rpacks.txt", "character")), repos="'"${CRAN_MIRROR}"'")'
RUN \
  cd /src && \
  R -e 'source("http://bioconductor.org/biocLite.R"); biocLite(sub("(.+)\\\\n","\\1", scan("biocLite.txt", "character")))'

RUN \
  cd /src && \
  pip3 --no-cache-dir install -r requirements.txt && \
  rm -rf /root/.cache

ADD ./code/ /code/
RUN \
  cd /code && \
  R CMD INSTALL MetDNA_0.99.12-3.tar.gz

