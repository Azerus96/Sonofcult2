# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    AI_PROGRESS_TOKEN = os.getenv('AI_PROGRESS_TOKEN')
    PROGRESS_DIR = 'progress'
    SESSION_TYPE = 'filesystem'
    MAX_CARDS = {
        'top': 3,
        'middle': 5,
        'bottom': 5
    }
    GAME_TIMEOUT = 300  # 5 минут на игру
