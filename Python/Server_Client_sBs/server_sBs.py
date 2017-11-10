################################################################################
#Program Description:
#This displays the motion vector data from the h.264 encoder on the picamera
#side by side.
#The Server side waits to recieve a connection. Once established, it takes 
#Images, does processing, and also displays the other frame it is listening for
################################################################################

################################################################################
#Required Libs
################################################################################
import pickle
import socket
import struct
import cv2
import sys
import time

from threading import Thread

from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np

import queue

################################################################################
#Variable Section
################################################################################

HOST = sys.argv[1]
PORT = 8082

camera = PiCamera()

ack_data = bytearray()

camera.resolution = (640, 480)
camera.framerate = 30
camera.vflip = True
camera.hflip = True
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(1)
image = np.empty((640 * 480 * 3,), dtype=np.uint8)
abort = False
image_q = queue.Queue(1)

################################################################################
#The Setup for the Pi Motion Vectors. Save Time frame number
def myfunc():
    global image_q
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array[:,:,1]
        try:
            image_q.put_nowait(image)
        except queue.Full:
            pass
        rawCapture.truncate(0)

#Setup our camera capture thread first
t = Thread(target=myfunc)
t.start()

#Not setup a socket, and listen
web_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
web_socket.bind((HOST, PORT))
print ('Server started on \'' + str(HOST) + ':' + str(PORT) + '\'')
web_socket.listen(10)

connection, _ = web_socket.accept()

connection_data = bytearray()
payload_size = struct.calcsize('L')

#Once the connection has been established we run this until termianted

while True:
    while len(connection_data) < payload_size:
        connection_data += connection.recv(4096)
    packed_msg_size = connection_data[:payload_size]
    connection_data = connection_data[payload_size:]
    msg_size = struct.unpack('L', packed_msg_size)[0]
    while len(connection_data) < msg_size:
        connection_data += connection.recv(4096)

    frame_data = connection_data[:msg_size]
    connection_data = connection_data[msg_size:]
    frame = pickle.loads(frame_data)
    try:
        OtherFrame = image_q.get(True,1.0)
    except queue.Empty:
        pass
    cv2.imshow('Left', frame)
    cv2.imshow('Right',OtherFrame)
    cv2.waitKey(1)
    #sendack
    connection_data = bytearray()
    connection.send(b'/xFF')

    
cv.destroyAllWindows()
