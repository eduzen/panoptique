import logging
from typing import Optional

import cv2
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

# Get an instance of a logger
logger = logging.getLogger(__name__)


class VideoCamera:
    device = 0
    quality = cv2.COLOR_BGR2BGRA  # cv2.COLOR_BGR2GRAY

    def __init__(self):
        self.camera = cv2.VideoCapture(self.device)

    def __del__(self):
        self.camera.release()

    @property
    def frame(self):
        _, image = self.camera.read()

        if image is None:
            raise RuntimeError

        return image

    @property
    def jpeg(self):
        _, jpeg = cv2.imencode(".jpg", self.frame)

        if jpeg is None:
            raise RuntimeError

        return jpeg

    def stream(self):
        while self.camera.isOpened:
            try:
                yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n%b\r\n\r\n" % self.jpeg.tobytes()
            except Exception:
                logger.exception("error")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/video")
async def main():
    stream = StreamingResponse(
        VideoCamera().stream(),
        media_type="multipart/x-mixed-replace;boundary=frame",
    )
    return stream
