FROM ubuntu:20.04
RUN apt update && DEBIAN_FRONTEND=noninteractive TZ="Europe/Rome" apt-get -y install tzdata && apt upgrade -y
RUN apt install -y python3.9 python3-pip
RUN python3.9 -m pip install --upgrade pip
RUN python3.9 -m pip install playwright
RUN playwright install
RUN playwright install-deps
RUN cp -r /root/.cache/ms-playwright/webkit-1630 /root/.cache/ms-playwright/webkit-1578
RUN apt-get install libmanette-0.2-0
ARG GATEWAY
ENV GATEWAY=$GATEWAY
ENV PYTHONUNBUFFERED=0
EXPOSE 8080
RUN apt update && apt install -y unzip zip curl wget build-essential
ADD ./requirements.lock /
RUN pip install -r /requirements.lock
ADD . /plugin
ENV PYTHONPATH=$PYTHONPATH:/plugin
WORKDIR plugin/services
CMD ["uvicorn", "services:app", "--host", "0.0.0.0", "--port", "8080"]