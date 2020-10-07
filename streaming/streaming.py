import logging
import time

import cv2

from .decorators import threaded

logger = logging.getLogger(__name__)


class RipCamera:
    def __init__(self, *args, **kwargs):
        self.video_capture = cv2.VideoCapture(0)

    @threaded
    def read_camera(self):
        if not self.video_capture.isOpened():
            raise RuntimeError()

        status, frame = self.video_capture.read()

        if status:
            return frame

        raise RuntimeError()

    def stream_camera(self):
        while True:
            frame = self.read_camera()
            status, jpeg = cv2.imencode(".jpg", frame)

            if not status or jpeg is None:
                raise RuntimeError

            time.sleep(0.017)
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n%b\r\n\r\n" % jpeg.tobytes()
