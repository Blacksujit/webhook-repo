import os
from flask import Flask
from app.config import DevelopmentConfig, ProductionConfig


def create_app():
    app = Flask(__name__)
    
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'production':
        config_class = ProductionConfig
    else:
        config_class = DevelopmentConfig
    
    app.config.from_object(config_class)
    
    return app