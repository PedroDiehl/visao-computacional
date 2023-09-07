import os
import logging
import roslibpy
from dotenv import load_dotenv
from CameraHelper import CameraHelper
from JoystickHelper import JoystickHelper
load_dotenv()


'''
Subscriber Test

@author Pedro Henrique Diehl
'''


logging_format = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=logging_format, level=logging.INFO)
log = logging.getLogger(__name__)


class SolverCenario1():
   def __init__(self, host: str, port: int):
      self.host = host
      self.port = port
      self.client: roslibpy.Ros = roslibpy.Ros(host=self.host, port=self.port)

   def joystick_talker(self):
      self.joystic_helper = JoystickHelper(
         self.client, 
         '/game/joy',
         'sensor_msgs/Joy'
      )
      return

   def camera_subscriber(self):
      self.camera_helper = CameraHelper(
         self.client, 
         '/game/cam1',
         'sensor_msgs/CompressedImage',
         self.joystic_helper
      )
      return

   def execute(self):
      self.joystick_talker()
      self.camera_subscriber()
      self.client.run_forever()
      return


if __name__ == '__main__':
   ROS_HOST: str = os.getenv('ROS_HOST') 
   ROS_PORT: int = int(os.getenv('ROS_PORT'))

   solver: SolverCenario1 = SolverCenario1(host=ROS_HOST, port=ROS_PORT)
   solver.execute()
