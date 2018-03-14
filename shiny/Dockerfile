FROM rpy2/rpy2:2.9.x

MAINTAINER Laurent Gautier <lgautier@gmail.com>, Xin Xiong <xiongxin20008@126.com>

ARG DEBIAN_FRONTEND=noninteractive
ARG CRAN_MIRROR=https://cran.rstudio.com/

# Install basic stuff
RUN apt-get update && apt-get install -y \
    vim-tiny \
    less \
    r-recommended \
    fonts-texgyre

# =====================================================================
# Shiny Server dev stuff + Shiny
# =====================================================================

RUN apt-get update && apt-get install -y \
    gdebi-core \
    pandoc \
    pandoc-citeproc \
    libcurl4-gnutls-dev \
    libcairo2-dev \
    libxt-dev \
    libssl-dev \
    libxml2-dev \
    cmake \
    # Pro-specific
    libpam0g-dev \
    openjdk-8-jre

# Download and install shiny server
RUN \
    cd /tmp && \
    wget --no-verbose https://download3.rstudio.org/ubuntu-12.04/x86_64/shiny-server-1.5.6.875-amd64.deb && \
    gdebi -n shiny-server-1.5.6.875-amd64.deb && \
    rm -f shiny-server-1.5.6.875-rh5-x86_64.rpm
	
# install R package, contains `shiny`
ADD ./package/ /src/
RUN \
    cd /src && \
    R -e 'install.packages(sub("(.+)\\\\n","\\1", scan("rpacks.txt", "character")), repos="'"${CRAN_MIRROR}"'")'

# install R package from github/zip file
#RUN \
#    R -e "devtools::install_github('rstudio/shiny-incubator')" && \
#    R -e "devtools::install_github('AnalytixWare/ShinySky')"

ADD ./github_unzip/ /github_unzip/
# RUN R -e 'install.packages(c("RJSONIO", "DT", "readr", "shinyjs"), repos="'"${CRAN_MIRROR}"'")'
RUN \
    R -e "devtools::install('/github_unzip/rstudio-shiny-incubator-b53511d', repos=NULL, type='source')" && \
    R -e "install.packages('/github_unzip/AnalytixWare-ShinySky-242ab16', repos=NULL, type='source')"

RUN \
    mkdir -p /srv/shiny-server/demo && \
    chmod -R 0777 /srv/shiny-server && \
    chown -R shiny:shiny /var/log/shiny-server &&\
    cp -R /usr/local/lib/R/site-library/shiny/examples/* /srv/shiny-server/demo && \
    rm -rf /var/lib/apt/lists/*
	
EXPOSE 3838

#USER shiny
