import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Define the base directory of the project
basedir = os.path.abspath(os.path.dirname(__file__))

# Ensure the database directory exists
# db_dir = os.path.join(basedir)
# if not os.path.exists(db_dir):
    # os.makedirs(db_dir)

db_dir = os.path.dirname(basedir)
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

# Define the default database path
db_path = os.path.join(basedir, 'soccer_cards_app.db')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret')
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('TEST_JWT_SECRET_KEY', 'test-jwt-secret')
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads_test')
    WTF_CSRF_ENABLED = False
