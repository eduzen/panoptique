FROM jjanzic/docker-python3-opencv
ENV PYTHONUNBUFFERED 1
RUN echo 'export PS1="\[\e[36m\]panshell>\[\e[m\] "' >> /root/.bashrc

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -U pip && pip install -r requirements.txt
COPY . /code/
