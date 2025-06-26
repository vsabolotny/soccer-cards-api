import pytest
import json
from app import create_app, db
from app.models.user import User

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')  # Assuming you have a 'testing' config
    testing_client = flask_app.test_client()

    # Establish an application context
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()

@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table(s)
    db.create_all()

    yield db  # this is where the testing happens!

    db.session.remove()
    db.drop_all()

def test_register_user_success(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted to (POST) with valid data
    THEN a new user should be created and a 201 status code returned
    """
    response = test_client.post('/auth/register',
                                json={'email': 'test@example.com', 'password': 'password123'})
    assert response.status_code == 201
    assert response.json['msg'] == 'User registered successfully'

    user = User.query.filter_by(email='test@example.com').first()
    assert user is not None
    assert user.email == 'test@example.com'

def test_register_user_existing_email(test_client, init_database):
    """
    GIVEN a Flask application configured for testing and a user already exists
    WHEN the '/register' page is posted to (POST) with an existing email
    THEN a 400 status code should be returned
    """
    # First, register a user
    test_client.post('/auth/register',
                     json={'email': 'existing@example.com', 'password': 'password123'})
    
    # Try to register the same user again
    response = test_client.post('/auth/register',
                                json={'email': 'existing@example.com', 'password': 'anotherpassword'})
    assert response.status_code == 400
    assert response.json['msg'] == 'User registration failed' # Or a more specific message like "Email already exists"

def test_login_user_success(test_client, init_database):
    """
    GIVEN a Flask application configured for testing and a registered user
    WHEN the '/login' page is posted to (POST) with valid credentials
    THEN an access token should be returned and a 200 status code
    """
    # Register a user first
    test_client.post('/auth/register',
                     json={'email': 'loginuser@example.com', 'password': 'password123'})

    # Attempt to login
    response = test_client.post('/auth/login',
                                json={'email': 'loginuser@example.com', 'password': 'password123'})
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_login_user_invalid_email(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST) with an invalid email
    THEN a 401 status code should be returned
    """
    response = test_client.post('/auth/login',
                                json={'email': 'nonexistent@example.com', 'password': 'password123'})
    assert response.status_code == 401
    assert response.json['msg'] == 'Bad email or password'

def test_login_user_invalid_password(test_client, init_database):
    """
    GIVEN a Flask application configured for testing and a registered user
    WHEN the '/login' page is posted to (POST) with an invalid password
    THEN a 401 status code should be returned
    """
    # Register a user first
    test_client.post('/auth/register',
                     json={'email': 'anotherlogin@example.com', 'password': 'correctpassword'})

    # Attempt to login with wrong password
    response = test_client.post('/auth/login',
                                json={'email': 'anotherlogin@example.com', 'password': 'wrongpassword'})
    assert response.status_code == 401
    assert response.json['msg'] == 'Bad email or password'
