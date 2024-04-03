import os
import string

SHORT_SIZE = 6
ALLOWED_SYMBOLS = string.ascii_letters + string.digits
SHORT_SYMBOLS_REGEXP = f'^[{ALLOWED_SYMBOLS}]*$'
MAX_SHORT_SIZE = 16
MAX_ORIGINAL_SIZE = 2048
REDIRECT_FUNCTION_NAME = 'redirect_view'
NUMBER_OF_REPETITIONS = 6


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_key')
