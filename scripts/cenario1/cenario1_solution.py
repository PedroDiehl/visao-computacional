import os
import cv2
import base64
import roslibpy
import numpy as np
from dotenv import load_dotenv
from JoystickHelper import JoystickHelper
from CamerasHelper import Camera1Helper, Camera2Helper

load_dotenv()


'''
Subscriber Test

@author Pedro Henrique Diehl
'''


class SolverCenario1(Camera1Helper, Camera2Helper, JoystickHelper):
   def __init__(self, host: str, port: int):
      self.host = host
      self.port = port
      self.subscribers: dict = {}

   def instantiate_client(self) -> None:
      self.client: roslibpy.Ros = roslibpy.Ros(host=self.host, port=self.port)
      return

   def setup(self) -> None:
      self.setup_listeners()
      self.setup_talkers()
      return 

   def setup_listeners(self) -> None:
      self.link_to_topic(
         topic_name='game/cam1', 
         message_type='sensor_msgs/CompressedImage'
      )
      self.subscribe_callback(
         topic_name='game/cam1',
         callback=self.process_camera1_message
      )

      self.link_to_topic(
         topic_name='game/cam2', 
         message_type='sensor_msgs/CompressedImage',
      )
      self.subscribe_callback(
         topic_name='game/cam2',
         callback=self.process_camera2_message
      )

      return

   def setup_talkers(self) -> None:
      self.link_to_topic(
         topic_name='game/joy', 
         message_type='sensor_msgs/Joy',
      )

      return

   def link_to_topic(self, topic_name: str, message_type: str) -> None:
      self.subscribers[topic_name]: roslibpy.Topic = roslibpy.Topic(
         self.client, 
         topic_name, 
         message_type
      )

      return

   def subscribe_callback(self, topic_name: str, callback: callable) -> None:
      self.subscribers[topic_name].subscribe(callback)

      return

   def process_camera1_message(self, message: roslibpy.Message) -> None:
      image_np = self.ros_message_to_image(message)

      self.manipulate_cam1_image(image_np)

      cv2.imshow('CAM 1', image_np)
      cv2.waitKey(1)

      return

   def process_camera2_message(self, message: roslibpy.Message) -> None:
      image_np = self.ros_message_to_image(message)

      self.manipulate_cam2_image(image_np)

      cv2.imshow('CAM 2', image_np)
      cv2.waitKey(1)

      return

   def ros_message_to_image(self, message: roslibpy.Message) -> np.ndarray:
      base64_bytes = message['data'].encode('ascii')

      image_bytes = base64.b64decode(base64_bytes)

      np_array = np.frombuffer(image_bytes, dtype=np.uint8)

      return cv2.imdecode(np_array, cv2.IMREAD_COLOR)

   def run(self) -> None:
      self.client.run_forever()

   def execute(self) -> None:
      self.instantiate_client()
      self.setup()
      self.run()


if __name__ == '__main__':
   ROS_HOST: str = os.getenv('ROS_HOST') 
   ROS_PORT: int = int(os.getenv('ROS_PORT'))

   solver: SolverCenario1 = SolverCenario1(host=ROS_HOST, port=ROS_PORT)
   solver.execute()
