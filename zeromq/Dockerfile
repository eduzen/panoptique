FROM python:3.8
EXPOSE 5555

RUN apt-get update && apt-get install -y \
    python3-opencv \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer1.0-dev

RUN pip install pyzmq pillow
RUN pip install opencv-python
WORKDIR /code/
