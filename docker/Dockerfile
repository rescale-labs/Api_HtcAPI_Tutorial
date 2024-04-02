FROM python:3.10
RUN apt-get -qq update \
    && apt-get -y install ffmpeg libsm6 libxext6

RUN pip install --upgrade pip \
    && pip install opencv-python \
    && pip install rescale-htc-storage -U \
        --extra-index-url http://rescale-htc-cli-agae5ucedee8kohtaet8naekx.s3-website-eu-west-1.amazonaws.com \
        --trusted-host rescale-htc-cli-agae5ucedee8kohtaet8naekx.s3-website-eu-west-1.amazonaws.com

COPY face_tagger/face_tagger.py /opt/face_tagger.py