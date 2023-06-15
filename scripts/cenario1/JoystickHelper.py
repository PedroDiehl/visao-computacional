import roslibpy

class JoystickHelper:
   def __init__(self):
      pass

   def joystick_action(self, talker: roslibpy.Topic) -> None:
      joystick_message: roslibpy.Message = roslibpy.Message({
         'axes': [1, 2],
         'buttons': [0]
      })

      talker.publish(joystick_message)

      return
