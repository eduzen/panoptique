FROM python:3.8

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.4

RUN echo 'export PS1="\[\e[36m\]panshell>\[\e[m\] "' >> /root/.bashrc

RUN apt-get update && apt-get install -y \
    python3-opencv \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer1.0-dev

RUN pip install poetry==$POETRY_VERSION

WORKDIR /code

COPY pyproject.toml poetry.lock /code/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /code

CMD ["gunicorn", "panoptique.wsgi", "--log-level", "debug", "--workers", "1", "--threads", "4", "-k", "gevent"]
