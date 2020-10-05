import cv2

from .decorators import threaded

video_capture = cv2.VideoCapture(0)


@threaded
def read_camera():
    if not video_capture.isOpened():
        raise RuntimeError()

    status, frame = video_capture.read()

    if status:
        return frame

    raise RuntimeError()


def stream_camera():
    while True:
        frame = read_camera()
        status, jpeg = cv2.imencode(".jpg", frame)

        if not status or jpeg is None:
            raise RuntimeError

        yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n%b\r\n\r\n" % jpeg.tobytes()
