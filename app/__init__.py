import os
from flask import Flask
from app.config import DevelopmentConfig, ProductionConfig
from app.routes import webhook_bp


def create_app():
    # Get the directory where this file is located
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # Set template and static folders relative to the app directory
    template_folder = os.path.join(basedir, '..', 'templates')
    static_folder = os.path.join(basedir, '..', 'static')
    
    app = Flask(__name__, 
                template_folder=template_folder,
                static_folder=static_folder)
    
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'production':
        config_class = ProductionConfig
    else:
        config_class = DevelopmentConfig
    
    app.config.from_object(config_class)
    
    # Initialize database (handle failures gracefully)
    try:
        from app.db import init_db
        init_db(app)
        print("✅ Database connected successfully!")
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")
        print("App will run without database functionality")
    
    # Register blueprint
    app.register_blueprint(webhook_bp)
    
    return app