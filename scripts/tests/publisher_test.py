import os
import cv2
from dotenv import load_dotenv
load_dotenv()


'''
Publisher Test
'''


ROS_IP: str = os.getenv('ROS_IP')
ROS_PORT: str = os.getenv('ROS_PORT')

print(ROS_IP)
print(ROS_PORT)
