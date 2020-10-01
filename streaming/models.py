import datetime
import logging

import cv2

# Get an instance of a logger
logger = logging.getLogger(__name__)


class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    @property
    def frame(self):
        _, image = self.video.read()

        if image is None:
            raise RuntimeError

        return image

    @property
    def jpeg(self):
        _, jpeg = cv2.imencode(".jpg", self.frame)

        if jpeg is None:
            raise RuntimeError

        return jpeg

    def grab_contours(self, cnts):
        # if the length the contours tuple returned by cv2.findContours
        # is '2' then we are using either OpenCV v2.4, v4-beta, or
        # v4-official
        if len(cnts) == 2:
            cnts = cnts[0]

        # if the length of the contours tuple is '3' then we are using
        # either OpenCV v3, v4-pre, or v4-alpha
        elif len(cnts) == 3:
            cnts = cnts[1]

        # otherwise OpenCV has changed their cv2.findContours return
        # signature yet again and I have no idea WTH is going on
        else:
            raise Exception(
                "Contours tuple must have length 2 or 3, "
                "otherwise OpenCV changed their cv2.findContours return "
                "signature yet again. Refer to OpenCV's documentation "
                "in that case"
            )

        # return the actual contours array
        return cnts

    def process(self):
        self.timestamp = datetime.datetime.now()
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        blur_size = (21, 21)
        gray = cv2.GaussianBlur(gray, blur_size, 0)

        if self.avg is None:
            logger.warning("[INFO] starting background model...")
            self.avg = gray.copy().astype("float")
            return

        # accumulate the weighted average between the current frame and
        # previous frames, then compute the difference between the current
        # frame and running average
        self.frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(self.avg))
        cv2.accumulateWeighted(gray, self.avg, 0.5)

        # threshold the delta image, dilate the thresholded image to fill
        # in holes, then find contours on thresholded image
        delta_thresh = 5
        thresh = cv2.threshold(self.frameDelta, delta_thresh, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = self.grab_contours(cnts)

        min_area = 5000
        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < min_area:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.empty = False

        # draw the text and timestamp on the frame
        ts = self.timestamp.isoformat()
        cv2.putText(
            self.frame,
            f"Room Status: {'empty' if self.empty else 'occupied'}",
            (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            2,
        )
        cv2.putText(
            self.frame,
            ts,
            (10, self.frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.35,
            (0, 0, 255),
            1,
        )

        # check to see if the room is occupied
        if not self.empty:
            logger.warning("mmm if occupied")
            # save occupied frame
            cv2.imwrite(
                f"assets/picamera/talkingraspi_{self.motionCounter}.jpg".format(),
                self.frame,
            )

            # check to see if enough time has passed between uploads
            min_upload_seconds = 0.5
            min_motion_frames = 9
            if (self.timestamp - self.lastUploaded).seconds >= min_upload_seconds:
                logger.warning(self.motionCounter)
                logger.warning(self.motionCounter)

                # increment the motion counter
                self.motionCounter += 1

                # check to see if the number of frames with consistent motion is
                # high enough
                if self.motionCounter >= min_motion_frames:
                    logger.warning(self.motionCounter)
                    logger.warning(min_motion_frames)

                    self.show_image(True)
                    logger.warning("ALGO CAMBIOOOOO")

                    # update the last uploaded timestamp and reset the motion
                    # counter
                    self.lastUploaded = self.timestamp
                    self.motionCounter = 0

        # otherwise, the room is not occupied
        else:
            self.motionCounter = 0

    def show_image(self, show=False):
        if not show:
            return
        cv2.imshow("Security Feed", self.frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            raise KeyboardInterrupt

    def analize(self, show_img=False):
        self.empty = True
        self.lastUploaded = datetime.datetime.now()
        self.motionCounter = 0
        self.avg = None
        self.motionCounter = 0
        while self.video.isOpened:
            try:
                self.process()
            except:  # NOQA
                break

    def stream(self):
        while self.video.isOpened:
            try:
                yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n%b\r\n\r\n" % self.jpeg.tobytes()
            except Exception:
                logger.exception("error")
                break
