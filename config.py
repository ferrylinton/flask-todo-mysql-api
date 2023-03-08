import os
from dotenv import load_dotenv
load_dotenv()

class Config(object):

    DEBUG = os.environ.get('DEBUG', False)
    JSON_SORT_KEYS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'flask-todo-mysql-api')

    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_DATABASE = os.environ.get('DB_DATABASE')
    DB_POOL_NAME = os.environ.get('DB_POOL_NAME')
    DB_POOL_SIZE = int(os.environ.get('DB_POOL_SIZE', '5'))

