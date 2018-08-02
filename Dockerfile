# Docker file for the dcm_tagExtract plugin app
#
# Build with
#
#   docker build -t <name> .
#
# For example if building a local version, you could do:
#
#   docker build -t local/pl-pfdicom_tagsub .
#
# In the case of a proxy (located at 192.168.13.14:3128), do:
#
#    docker build --build-arg http_proxy=http://192.168.13.14:3128 --build-arg UID=$UID -t local/pl-pfdicom_tagsub .
#
# To run an interactive shell inside this container, do:
#
#   docker run -ti --entrypoint /bin/bash local/pl-pfdicom_tagsub
#


FROM fnndsc/ubuntu-python3:latest
MAINTAINER fnndsc "dev@babymri.org"

ENV APPROOT="/usr/src/dcm_tagSub"  VERSION="0.1"
COPY ["dcm_tagSub", "${APPROOT}"]
COPY ["requirements.txt", "${APPROOT}"]

WORKDIR $APPROOT

# Pass a UID on build command line (see above) to set internal UID
ARG UID=1001
ENV UID=$UID

RUN apt-get update                                                      \
  && apt-get install sudo                                               \
  && useradd -u $UID -ms /bin/bash localuser                            \
  && addgroup localuser sudo                                            \
  && echo "localuser:localuser" | chpasswd                              \
  && adduser localuser sudo                                             \
  && apt-get install -y libmysqlclient-dev                              \
  && apt-get install -y libssl-dev libcurl4-openssl-dev                 \
  && apt-get install -y bsdmainutils vim net-tools inetutils-ping       \
  && apt-get install -y python3-tk                                      \
  && pip install --upgrade pip                                          \
  && pip install -r requirements.txt

CMD ["dcm_tagSub.py", "--help"]