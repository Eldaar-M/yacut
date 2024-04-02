import os
import string

GENERATION_NUMBER = 6
ALLOWED_SYMBOLS = string.ascii_letters + string.digits
URL_SYMBOLS_REGEXP = f'^[{ALLOWED_SYMBOLS}]*$'
MAX_SHORT_SIZE = 16
MAX_ORIGINAL_SIZE = 2048
REDIRECT_FUNCTION_NAME = 'redirect_view'


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_key')
