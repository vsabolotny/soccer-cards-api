import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'soccer_cards_app.db')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'you_should_change_this')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{db_path}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'ba5d152a234ae39176e5d1ed04e3396ab0188e4264c08d2db36ddb10449075ef')
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads') 

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('TEST_JWT_SECRET_KEY', 'test_jwt_secret_key')
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads_test')
    WTF_CSRF_ENABLED = False