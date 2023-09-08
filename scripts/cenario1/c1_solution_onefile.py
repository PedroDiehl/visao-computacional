import os
import cv2
import time
import base64
import logging
import roslibpy
import numpy as np
from dotenv import load_dotenv
load_dotenv()


'''
Solução em 1 arquivo
'''


logging_format = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=logging_format, level=logging.INFO)
log = logging.getLogger(__name__)

client = roslibpy.Ros(host=os.getenv('ROS_HOST'), port=int(os.getenv('ROS_PORT')))

talker = roslibpy.Topic(client, '/game/joy', 'sensor_msgs/Joy')

def main(image: np.ndarray):
   cv2.imshow('Original', image)

   blurred = cv2.GaussianBlur(image, (5, 5), 0)
   gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

   difference, max_difference = calculate_difference(gray)

   mapped_difference = difference / max_difference
   draw_arrow(mapped_difference, image)
   cv2.waitKey(1)

   joystick_message = roslibpy.Message({
      'axes': [mapped_difference, 0.2],
      'buttons': [0]
   })

   talker.publish(joystick_message)

   time.sleep(1)
   return

def draw_arrow(mapped_difference: float, image: np.ndarray):
   # Draw a arrow scaled by mapped_difference
   height, width, _ = image.shape
   arrow_end = (int(width / 2), int(height / 2))
   arrow_start = (int(width / 2 + mapped_difference * 500), int(height / 2))
   cv2.arrowedLine(image, arrow_start, arrow_end, (0, 0, 255), thickness=5)

   # Display the result
   cv2.imshow('FLECHA', image)

   return

def calculate_difference(image: np.ndarray):
   # Split the identified path image into left and right sides and crop the top
   height, width, _ = image.shape
   left_side = image[0:int(height / 2), int(width / 4):int(width / 2)]
   right_side = image[0:int(height / 2), int(width / 2):int(3 / 4 * width)]

   # Calculate the number of white pixels in each side
   left_white_pixels = np.sum(left_side == 255)
   right_white_pixels = np.sum(right_side == 255)

   # Show the left and right sides
   cv2.imshow('Left Side', left_side)
   cv2.imshow('Right Side', right_side)

   # Return the difference between the number of white pixels in each side
   difference = left_white_pixels - right_white_pixels
   max_difference = left_side.shape[0] * left_side.shape[1]

   return (difference, max_difference)

def receive_image(message):
   base64_bytes = message['data'].encode('utf-8')
   image_bytes = base64.b64decode(base64_bytes)
   np_array = np.frombuffer(image_bytes, dtype=np.uint8)

   image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
   main(image)
   return


subscriber = roslibpy.Topic(client, '/game/cam1', 'sensor_msgs/CompressedImage')
subscriber.subscribe(receive_image)

client.run_forever()
