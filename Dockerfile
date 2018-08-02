# Docker file for the dcm_tagSub plugin app

FROM fnndsc/ubuntu-python3:latest
MAINTAINER fnndsc "dev@babymri.org"

ENV APPROOT="/usr/src/dcm_tagSub"  VERSION="0.1"
COPY ["dcm_tagSub", "${APPROOT}"]
COPY ["requirements.txt", "${APPROOT}"]

WORKDIR $APPROOT

RUN pip install -r requirements.txt

CMD ["dcm_tagSub.py", "--help"]