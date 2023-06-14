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
ROS_PORT: str = os.getenv('ROS_PORT')

client: roslibpy.Ros = roslibpy.Ros(host=ROS_HOST, port=int(ROS_PORT))

def receive_image(message: roslibpy.Message):
   base64_bytes = message['data'].encode('ascii')
   image_bytes = base64.b64decode(base64_bytes)
   np_array = np.frombuffer(image_bytes, dtype=np.uint8)

   image_numpy = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

   cv2.imshow('image', image_numpy)
   cv2.waitKey(1)

   return

listener: roslibpy.Topic = roslibpy.Topic(client, '/game/cam1', 'sensor_msgs/CompressedImage')
listener.subscribe(receive_image)

client.run_forever()
