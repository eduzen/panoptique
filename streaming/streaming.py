import datetime as dt
import logging
import time

import cv2

from .decorators import threaded

logger = logging.getLogger(__name__)


class RipCamera:

    video_capture = cv2.VideoCapture(0)
    last_access = 0

    def __init__(self, *args, **kwargs):
        if not self.__class__.video_capture.isOpened():
            self.__class__.video_capture = cv2.VideoCapture(0)

        self.__class__.last_access = dt.datetime.now().isoformat()

    def __del__(self):
        self.__class__.video_capture.release()

    @threaded
    def read_camera(self):
        status, frame = self.__class__.video_capture.read()
        if status:
            return frame

        raise RuntimeError()

    def stream_camera(self):
        self.last_access = time.process_time()
        while True:
            if not self.video_capture.isOpened():
                continue

            frame = self.read_camera()

            status, jpeg = cv2.imencode(".jpg", frame)

            if not status or jpeg is None:
                raise RuntimeError

            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n%b\r\n\r\n" % jpeg.tobytes()
            time.sleep(0.025)
