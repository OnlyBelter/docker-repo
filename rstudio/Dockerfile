FROM onlybelter/rpy2-docker
MAINTAINER Laurent Gautier <lgautier@gmail.com>, Xin Xiong <xiongxin20008@126.com>
# https://github.com/rocker-org/rocker-versioned/blob/master/rstudio/3.4.4/Dockerfile

ENV RSTUDIO_VERSION=1.1.442
ENV PATH=/usr/lib/rstudio-server/bin:$PATH
ARG CRAN_MIRROR=https://cran.rstudio.com/

RUN cd /src && \
  rm * && \
  apt-get install psmisc && \
  wget https://download2.rstudio.org/rstudio-server-1.1.442-amd64.deb && \
  dpkg -i rstudio-server-1.1.442-amd64.deb && \
  rm rstudio-server-*-amd64.deb

RUN set -e \
      && useradd -m -d /home/rstudio rstudio \
      && echo rstudio:rstudio \
        | chpasswd

#RUN R -e 'devtools::install_github("rajarshi/cdkr", subdir="rcdklibs")' && \
#  R -e 'devtools::install_github("rajarshi/cdkr", subdir="rcdk")'

ADD ./package/ /src/
RUN \
  cd /src && \
  R -e 'install.packages(sub("(.+)\\\\n","\\1", scan("rpacks.txt", "character")), repos="'"${CRAN_MIRROR}"'")'

#RUN \
#  cd /src && \
#  R -e 'source("http://bioconductor.org/biocLite.R"); biocLite(sub("(.+)\\\\n","\\1", scan("biocLite.txt", "character")))'

EXPOSE 8787

# No chown will cause "RStudio Initalization Error"
# "Error occurred during the transmission"; RStudio will not load.
RUN addgroup rstudio staff && \
  chown rstudio:rstudio /home/rstudio && \
  chmod -R 0777 /home/rstudio

CMD ["/usr/lib/rstudio-server/bin/rserver", "--server-daemonize=0", "--server-app-armor-enabled=0"]
