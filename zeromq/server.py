import logging
import time

import cv2
import zmq

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

camera = cv2.VideoCapture(0)
time.sleep(1)
logger.debug("Starting %s" % "data")

while camera.isOpened():
    try:
        (grabbed, frame) = camera.read()

        if not grabbed:
            time.sleep(0.01)
            continue

        # frame = cv2.resize(frame, (640, 480))
        # data = {"frame": frame}

        socket.send_pyobj(frame)

        time.sleep(0.01)
    except KeyboardInterrupt:
        camera.release()
        cv2.destroyAllWindows()
        logger.debug("\n\nBye bye\n")
        break

socket.close()
context.term()
