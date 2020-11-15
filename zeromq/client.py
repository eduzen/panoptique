import logging
from time import sleep, time

import zmq
from PIL import Image

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.SUB)
socket.connect("tcp://zeromq:5555")
socket.subscribe("")
logger.debug("edu")

sleep(1)

for request in range(10):
    #  Get the reply.
    frame = socket.recv_pyobj()
    # logger.debug(frame['frame'])
    img = Image.fromarray(frame, "RGB")
    img.save(f"/code/testing/img{time()}.png")
    # print("Received reply %s [ %s ]" % (request, message))


# while True:
#     print("Sending request …")
#     topic = socket.recv_string()

#     frame = socket.recv_pyobj()
#     logger.debug(frame)
#     cv2.imshow('frame', frame['frame'])
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# context = zmq.Context()
# footage_socket = context.socket(zmq.SUB)
# footage_socket.connect('tcp://zeromq:5555')
# # footage_socket.setsockopt_string(zmq.SUBSCRIBE, '')

# while True:
#     try:
#         msg = src.recv_pyobj()
#         # frame = footage_socket.recv_string()
#         logger.debug(msg)
#         ts = msg['ts']
#         frame = msg['frame']
#         # img = base64.b64decode(frame)
#         npimg = np.fromstring(img, dtype=np.uint8)
#         source = cv2.imdecode(npimg, 1)
#         cv2.imshow("image", source)
#         cv2.waitKey(1)

#     except KeyboardInterrupt:
#         cv2.destroyAllWindows()
#         print("\n\nBye bye\n")
#         break
