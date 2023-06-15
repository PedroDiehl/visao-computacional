import os
import cv2
import base64
import roslibpy
import numpy as np
from dotenv import load_dotenv
load_dotenv()


'''
Subscriber Test

@author Pedro Henrique Diehl
'''


ROS_HOST: str = os.getenv('ROS_HOST')
ROS_PORT: int = int(os.getenv('ROS_PORT'))


client: roslibpy.Ros = roslibpy.Ros(host=ROS_HOST, port=ROS_PORT)

def receive_message_from_cam1(message: roslibpy.Message):
   base64_bytes = message['data'].encode('ascii')
   image_bytes = base64.b64decode(base64_bytes)
   np_array = np.frombuffer(image_bytes, dtype=np.uint8)

   image_np = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

   cv2.imshow('CAM 1', image_np)
   cv2.waitKey(1)

   return

def receive_message_from_cam2(message: roslibpy.Message):
   base64_bytes = message['data'].encode('ascii')
   image_bytes = base64.b64decode(base64_bytes)
   np_array = np.frombuffer(image_bytes, dtype=np.uint8)

   image_np = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

   cv2.imshow('CAM 2', image_np)
   cv2.waitKey(1)

   return

listener_cam1: roslibpy.Topic = roslibpy.Topic(client, '/game/cam1', 'sensor_msgs/CompressedImage')
listener_cam1.subscribe(receive_message_from_cam1)

listener_cam2: roslibpy.Topic = roslibpy.Topic(client, '/game/cam2', 'sensor_msgs/CompressedImage')
listener_cam2.subscribe(receive_message_from_cam2)

client.run_forever()
