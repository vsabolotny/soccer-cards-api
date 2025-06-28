from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config, TestingConfig # Correctly import your configs
import os

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    if config_name == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)

    # Ensure upload folders exist
    # This needs to be done after app.config is populated.
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # For testing, UPLOAD_FOLDER is also in TestingConfig. 
    # If tests create files, this folder should exist.
    # The previous logic for creating uploads_test during test setup (pytest fixture or globally)
    # might be more robust if tests run in parallel or specific test setup is needed.
    # However, creating it here if in 'testing' mode is also an option.
    if config_name == 'testing':
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
             os.makedirs(app.config['UPLOAD_FOLDER'])


    db.init_app(app)
    JWTManager(app)

    # Register blueprints
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.routes.cards import bp as cards_bp
    app.register_blueprint(cards_bp, url_prefix='/api')

    # Conditional db.create_all() for non-testing environments
    if config_name != 'testing':
        with app.app_context(): # Ensure we are within an app context for db operations
            try:
                db.create_all()
            except Exception as e:
                pass
    
    return app
