import os
from flask import Flask
import logging
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler
from mysql.connector.pooling import MySQLConnectionPool
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from .controllers import register_routes


connection_pool = MySQLConnectionPool(
                    pool_name=Config.DB_POOL_NAME,
                    pool_size=Config.DB_POOL_SIZE,
                    host=Config.DB_HOST,
                    database=Config.DB_DATABASE,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    jwt = JWTManager(app)

    configure_logging(app)
    register_routes(app)
    
    return app

def configure_logging(app):

    LOGS_FOLDER = 'logs'
    
    # Create logs folder
    isExist = os.path.exists(LOGS_FOLDER)
    if not isExist:
        os.makedirs(LOGS_FOLDER)
        print("logs directory is created!")

    # Deactivate the default flask logger so that log messages don't get duplicated 
    app.logger.removeHandler(default_handler)

    # Create a file handler object
    file_handler = RotatingFileHandler(f'{LOGS_FOLDER}/app.log', maxBytes=16384, backupCount=10)

    # Set the logging level of the file handler object so that it logs INFO and up
    file_handler.setLevel(logging.DEBUG)

    # Create a file formatter object
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]')

    # Apply the file formatter object to the file handler object
    file_handler.setFormatter(file_formatter)

    # Add file handler object to the logger
    app.logger.addHandler(file_handler)