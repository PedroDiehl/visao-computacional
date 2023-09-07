import os
import time
import roslibpy
from dotenv import load_dotenv
load_dotenv()


'''

'''


class JoystickHelper:
   def __init__(self, client: roslibpy.Ros, topic_name: str, topic_message: str):
      self.talker: roslibpy.Topic = roslibpy.Topic(client, topic_name, topic_message)

   def joystick_action(self, difference: int, max_difference: int):
      #print(difference)
      #print(max_difference)
      axes = self.calculate_axis_power(difference, max_difference)
      print(axes)

      joystick_message: roslibpy.Message = roslibpy.Message({
         'axes': axes, # Values between -1 and 1 - The first value is the speed and the second is the steering
         'buttons': [0] # The code doesn't use any buttons
      })

      self.talker.publish(joystick_message)
      time.sleep(3)

      return 

   def calculate_axis_power(self, difference: int, max_difference: int):
      # If difference is negative, the car is on the left side of the road and the steering value must be positive
      # If difference is positive, the car is on the right side of the road and the steering value must be negative
      # If difference is zero, the car is on the center of the road and the steering value must be zero
      mapped_difference = difference / max_difference

      return [mapped_difference, 0.02]


if __name__ == '__main__':
   ROS_HOST: str = os.getenv('ROS_HOST') 
   ROS_PORT: int = int(os.getenv('ROS_PORT'))

   joystic_helper: JoystickHelper = JoystickHelper(host=ROS_HOST, port=ROS_PORT)
