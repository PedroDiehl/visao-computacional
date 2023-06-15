import os
import cv2
import base64
import roslibpy
import numpy as np
from dotenv import load_dotenv
from CamerasHelper import Camera1Helper, Camera2Helper

load_dotenv()


'''
Subscriber Test

@author Pedro Henrique Diehl
'''


class Solver1(Camera1Helper, Camera2Helper):
   def __init__(self, host: str, port: int):
      self.host = host
      self.port = port
      self.listeners: dict = {}

   def setup_cam_views(self) -> None:
      self.subscribe_to_topic(cam_number=1, callback=self.receive_cam1_message)
      self.subscribe_to_topic(cam_number=2, callback=self.receive_cam2_message)

      return

   def subscribe_to_topic(self, cam_number: int, callback: callable) -> None:
      self.listeners[cam_number]: roslibpy.Topic = roslibpy.Topic(
         self.client, 
         f'game/cam{cam_number}', 
         'sensor_msgs/CompressedImage'
      )

      self.listeners[cam_number].subscribe(callback)

      return

   def receive_cam1_message(self, message: roslibpy.Message) -> None:
      image_np = self.ros_message_to_cv2_image(message)

      self.process_cam1_image(image_np)

      cv2.imshow('CAM 1', image_np)
      cv2.waitKey(1)

      return

   def receive_cam2_message(self, message: roslibpy.Message) -> None:
      image_np = self.ros_message_to_cv2_image(message)

      self.process_cam2_image(image_np)

      cv2.imshow('CAM 2', image_np)
      cv2.waitKey(1)

      return

   def ros_message_to_cv2_image(self, message: roslibpy.Message) -> np.ndarray:
      base64_bytes = message['data'].encode('ascii')

      image_bytes = base64.b64decode(base64_bytes)

      np_array = np.frombuffer(image_bytes, dtype=np.uint8)

      return cv2.imdecode(np_array, cv2.IMREAD_COLOR)

   def instantiate_client(self):
      self.client: roslibpy.Ros = roslibpy.Ros(host=self.host, port=self.port)
      return

   def run(self):
      self.client.run_forever()

   def execute(self):
      self.instantiate_client()
      self.setup_cam_views()
      self.run()

if __name__ == '__main__':
   ROS_HOST: str = os.getenv('ROS_HOST') 
   ROS_PORT: int = int(os.getenv('ROS_PORT'))

   solver: Solver1 = Solver1(host=ROS_HOST, port=ROS_PORT)
   solver.execute()
