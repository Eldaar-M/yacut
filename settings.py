import os

GENERATION_NUMBER = 6
URL_SYMBOLS_REGEXP = '^[A-Za-z0-9]*$'
MAX_URL_SIZE = 16


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_key')
