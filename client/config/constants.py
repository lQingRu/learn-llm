import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

try:
    API_URL = os.environ['API_URL']
except KeyError:
    API_URL = None