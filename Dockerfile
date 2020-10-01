# FROM arm32v7/python:3.8
FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.0.10
ENV VIRTUAL_ENV=/opt/venv

# We're creating virtualenv explicitly here, as seen here:
# https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
RUN pip install -U pip && python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
WORKDIR /code

RUN apt-get update && apt-get install -y \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer1.0-dev

RUN pip install poetry==$POETRY_VERSION

COPY pyproject.toml poetry.lock ./

RUN poetry install

RUN echo 'export PS1="\[\e[36m\]panshell>\[\e[m\] "' >> /root/.bashrc

COPY . /code/
