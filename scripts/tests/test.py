import os
from dotenv import load_dotenv
load_dotenv()

test = os.getenv('MY_VARIABLE')

print(test)
