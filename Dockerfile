FROM python:3.9-slim
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