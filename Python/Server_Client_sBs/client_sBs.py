################################################################################
#Program Description:
#This displays the motion vector data from the h.264 encoder on the picamera
#side by side.
#The Client side just sends the data to the host after minimal processing
#To be displayed at the same time.
################################################################################

################################################################################
#Required Libs
################################################################################
import cv2
import pickle
import socket
import struct
from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np
import time
import sys

################################################################################
#Variable Section
################################################################################

HOST = sys.argv[1]
PORT = 8082

MotionQueue = queue.Queue(10)

ack_data = bytearray()

image = np.zeros((77,104), dtype=(np.uint8,1))

################################################################################
#The Class for the Pi Motion Vectors. Save Time frame number
class DetectMotion(PiMotionAnalysis):
    def analyze(self, a):
        global freame_count
        freame_count = freame_count +1
        Data = (freame_count%128 , 0 ,int((time.time()*100)%65536))
        send_data = np.copy(a)
        send_data[76,103] = Data
        try:
            MotionQueueRIGHT.put_nowait(send_data)
        except queue.Full:
            pass


#setup the camera at the max resoultion for 30fps to get motion data
with picamera.PiCamera() as camera:
    camera.resolution = (1640, 1232)
    camera.framerate = 30
    camera.vflip = True
    camera.hflip = True
    camera.start_recording('result.h264', format='h264', motion_output=DetectMotion(camera))  

#Connect to the server 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

#Run until quit.
while True
    try:
        image = MotionQueueRIGHT.get(True,0.2)
        image_data = pickle.dumps(image)
        client_socket.sendall(struct.pack('L', len(image_data)) + image_data)
        ack_data = client_socket.recv(10)
    except queue.Empty:
        pass

