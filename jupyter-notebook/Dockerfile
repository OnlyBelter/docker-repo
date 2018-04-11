FROM jupyter/datascience-notebook
MAINTAINER Xin Xiong <xiongxin20008@126.com>

ARG CRAN_MIRROR=https://cran.rstudio.com/

USER root

# install Java
RUN \
  apt-get update -qq && \
  apt-get install -y openjdk-8-jdk  && \
  apt-get install -y mlocate && updatedb && \
  rm -rf /var/lib/apt/lists/*

RUN \
  ln -s /usr/lib/jvm/java-8-openjdk-amd64/include/jni.h /opt/conda/include/ && \
  ln -s /usr/lib/jvm/java-8-openjdk-amd64/include/linux/jni_md.h /opt/conda/include/  && \
  ln -s /usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server/libjvm.so /usr/lib/ && \  
  R CMD javareconf

# install rdkit
RUN apt-get update -qq && \
  apt-get install -y python-rdkit librdkit1 rdkit-data && \
  rm -rf /var/lib/apt/lists/*

ADD ./package/ /src/

# link lib
RUN \
  ln -s /opt/conda/lib/libpcre.so /usr/lib/  && \
  ln -s /opt/conda/lib/liblzma.so /usr/lib/  && \
  ln -s /opt/conda/lib/libbz2.so /usr/lib/  && \
  ln -s /opt/conda/lib/libz.so /usr/lib/  && \
  ln -s /opt/conda/lib/libiconv.so /usr/lib/  && \
  ln -s /opt/conda/lib/libicuuc.so /usr/lib/  && \
 ln -s /opt/conda/lib/libicui18n.so /usr/lib/


RUN \
  cd /src && \
  R -e 'install.packages(sub("(.+)\\\\n","\\1", scan("rpacks.txt", "character")), repos="'"${CRAN_MIRROR}"'")'
#RUN \
#  cd /src && \
#  R -e 'source("http://bioconductor.org/biocLite.R"); biocLite(sub("(.+)\\\\n","\\1", scan("biocLite.txt", "character")))'

RUN \
  cd /src && \
  conda install -c openbabel openbabel
  #pip --no-cache-dir install -r requirements.txt && \
  #rm -rf /root/.cache

RUN conda install -c rdkit rdkit

USER jovyan
