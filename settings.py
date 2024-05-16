import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
IMAGE_PATH = os.getenv("IMAGE_PATH")