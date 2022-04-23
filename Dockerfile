FROM ubuntu:latest

MAINTAINER Amazon AI

RUN apt-get -y update && apt-get install -y --no-install-recommends \
        wget \
        python3.9 \
        nginx \
        ca-certificates \
    libevent-dev \
    python-all-dev \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install -r requirements.txt

ENV PYTHONBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

COPY /recommender_model/ /opt/program/

RUN chmod +x /opt/program/serve

WORKDIR /opt/program/