import os
from dotenv import load_dotenv
load_dotenv()


'''
Subscriber Test
'''


ROS_IP: str = os.getenv('ROS_IP')
ROS_PORT: str = os.getenv('ROS_PORT')

print(ROS_IP)
print(ROS_PORT)
