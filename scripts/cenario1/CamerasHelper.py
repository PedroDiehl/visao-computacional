import os
import cv2
import base64
import roslibpy
import numpy as np


'''

'''


class Camera1Helper:
   def __init__(self):
      pass

   def receive_cam1_message(self, message: roslibpy.Message) -> None:
      image_np = self.ros_message_to_cv2_image(message)
      cv2.imshow('CAM 1', image_np)
      cv2.waitKey(1)

      return

   def process_cam1_image(self, image: np.ndarray):
      return


class Camera2Helper:
   def __init__(self):
      pass

   def receive_cam2_message(self, message: roslibpy.Message) -> None:
      image_np = self.ros_message_to_cv2_image(message)
      cv2.imshow('CAM 2', image_np)
      cv2.waitKey(1)

      return

   def process_cam2_image(self, image: np.ndarray):
      return

