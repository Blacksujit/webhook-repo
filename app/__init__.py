import os
from flask import Flask
from app.config import config


def create_app():
    app = Flask(__name__)
    
    env = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[env])
    
    return app