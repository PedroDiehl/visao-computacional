import os
import cv2
import base64
import roslibpy
import numpy as np
from dotenv import load_dotenv
from JoystickHelper import JoystickHelper
load_dotenv()


'''

'''


class CameraHelper:
   def __init__(self, client: roslibpy.Ros, topic_name: str, topic_message: str, joystick: JoystickHelper):
      self.joystick = joystick
      self.subscriber = roslibpy.Topic(client, topic_name, topic_message)
      self.subscriber.subscribe(self.receive_image)

   def receive_image(self, message: roslibpy.Message):
      base64_bytes = message['data'].encode('utf-8')
      image_bytes = base64.b64decode(base64_bytes)
      np_array = np.frombuffer(image_bytes, dtype=np.uint8)

      image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
      self.handle_image(image)
      cv2.waitKey(1)
      return

   def handle_image(self, image: np.ndarray):
      cv2.imshow('Received Image', image)
      identified_path_image = self.identify_path(image)
      difference, max_difference = self.calculate_difference(identified_path_image)
      #print(difference, max_difference, difference / max_difference)
      self.joystick.joystick_action(difference, max_difference)

      mapped_difference = difference / max_difference
      self.draw_arrow(mapped_difference, image)

      return

   def draw_arrow(self, mapped_difference: float, image: np.ndarray):
      # Draw a arrow scaled by mapped_difference
      height, width, _ = image.shape
      arrow_end = (int(width / 2), int(height / 2))
      arrow_start = (int(width / 2 + mapped_difference * 500), int(height / 2))
      cv2.arrowedLine(image, arrow_start, arrow_end, (0, 0, 255), thickness=5)

      # Display the result
      cv2.imshow('FLECHA', image)

      return

   def identify_path(self, image: np.ndarray):
      # Apply gaussian blur to reduce noise
      blurred = cv2.GaussianBlur(image, (5, 5), 0)
      cv2.imshow('Blurred Image', blurred)

      # Gray scale the image
      gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
      cv2.imshow('Gray Image', gray)

      # Threshold the grayscale image to create a binary image
      _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

      # Find contours in the binary image
      contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      # Create a mask for white contours on a black background
      identified_path_image = np.zeros_like(blurred)

      for contour in contours:
         # Calculate the area of each contour
         area = cv2.contourArea(contour)

         # Filter contours based on area (adjust the threshold as needed)
         if area > 1000:
            # Draw the selected contour on the result image
            cv2.drawContours(identified_path_image, [contour], -1, (0, 255, 0), thickness=cv2.FILLED)

      # Display the result
      cv2.imshow('Identified Path', identified_path_image)

      return identified_path_image

   def calculate_difference(self, identified_path_image: np.ndarray):
      # Split the identified path image into left and right sides and crop the top
      height, width, _ = identified_path_image.shape
      left_side = identified_path_image[0:int(height / 2), int(width / 4):int(width / 2)]
      right_side = identified_path_image[0:int(height / 2), int(width / 2):int(3 / 4 * width)]

      # Calculate the number of white pixels in each side
      left_white_pixels = np.sum(left_side == 255)
      right_white_pixels = np.sum(right_side == 255)

      # Show the left and right sides
      cv2.imshow('Left Side', left_side)
      cv2.imshow('Right Side', right_side)

      # Return the difference between the number of white pixels in each side
      difference = left_white_pixels - right_white_pixels
      max_difference = left_side.shape[0] * left_side.shape[1] * 2 # Account for the negative values

      return (difference, max_difference)

if __name__ == '__main__':
   ROS_HOST: str = os.getenv('ROS_HOST') 
   ROS_PORT: int = int(os.getenv('ROS_PORT'))

   camera_helper: CameraHelper = CameraHelper(host=ROS_HOST, port=ROS_PORT)
