FROM onlybelter/rpy2-shiny

MAINTAINER Xin Xiong <xiongxin20008@126.com>

ARG DEBIAN_FRONTEND=noninteractive
ARG CRAN_MIRROR=https://mirrors.shu.edu.cn/CRAN/


ADD ./package/ /src/
# install R package, contains `shiny`
# ADD ./package/ /src/
RUN \
    cd /src && \
    R -e 'install.packages(sub("(.+)\\\\n","\\1", scan("rpacks.txt", "character")), repos="'"${CRAN_MIRROR}"'")'

RUN \
    # apt-get update && apt-get install -y subversion && \
    cd /src && \
    R -e 'source("biocLite.R"); library(BiocInstaller); \
          biocLite(sub("(.+)\\\\n", "\\1", scan("bioconductor.txt", "character")), dep=TRUE)'
RUN \ 
    mkdir /srv/shiny-server2 && \
    chown -R shiny:shiny /var/lib/shiny-server  && \
    chown -R shiny:shiny /srv/shiny-server2

EXPOSE 3838

USER shiny
