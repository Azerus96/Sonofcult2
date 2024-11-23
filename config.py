# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    AI_PROGRESS_TOKEN = os.getenv('AI_PROGRESS_TOKEN')
    PROGRESS_DIR = 'progress'
    SESSION_TYPE = 'filesystem'
    PORT = int(os.getenv('PORT', 10000))
