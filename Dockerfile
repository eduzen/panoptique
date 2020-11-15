FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.0.10
RUN echo 'export PS1="\[\e[36m\]panshell>\[\e[m\] "' >> /root/.bashrc

WORKDIR /code

RUN apt-get update && apt-get install -y \
    python3-opencv \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer1.0-dev

RUN pip install poetry==$POETRY_VERSION

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . /code/
