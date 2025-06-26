import pytest
import json
import os
from io import BytesIO
from app import create_app, db
from app.models.card import Card
from app.models.user import User # Assuming you might need it for auth in the future

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')
    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()

@pytest.fixture(scope='module')
def init_database(test_client):
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()

@pytest.fixture(scope='function') # Function scope to ensure clean slate for each test
def new_card_data(tmp_path):
    # Create dummy image files for testing uploads
    front_img_content = b"dummy front image data"
    back_img_content = b"dummy back image data"
    
    # It's better to let the service handle file saving, 
    # so we just provide BytesIO objects.
    # The service should save them to a configured upload folder.
    # For testing, this might be a temporary folder.

    return {
        'playerName': 'Test Player',
        'cardYear': 2023,
        'team': 'Test Team',
        'imageFront': (BytesIO(front_img_content), 'test_front.jpg'),
        'imageBack': (BytesIO(back_img_content), 'test_back.jpg')
    }

def test_add_card_success(test_client, init_database, new_card_data):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/cards' endpoint is posted to (POST) with valid card data and images
    THEN a new card should be created, images saved, and a 201 status code returned
    """
    response = test_client.post('/api/cards',
                                content_type='multipart/form-data',
                                data=new_card_data)
    assert response.status_code == 201
    json_data = response.json
    assert json_data['playerName'] == new_card_data['playerName']
    assert 'imageFrontUrl' in json_data
    assert 'imageBackUrl' in json_data

    # Verify card in DB
    card = Card.query.filter_by(player_name=new_card_data['playerName']).first()
    assert card is not None
    assert card.team == new_card_data['team']
    # Add assertions for image URLs if your service saves them with predictable names/paths
    # For example: assert os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], card.image_front_url))


def test_add_card_missing_data(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/cards' endpoint is posted to (POST) with missing data
    THEN a 400 or appropriate error status code should be returned
    """
    response = test_client.post('/api/cards',
                                content_type='multipart/form-data',
                                data={'playerName': 'Missing Info'})
    # This depends on how your app handles missing fields.
    # It might be a 400, 422, or 500 if not handled gracefully.
    # For this example, let's assume it's a 500 due to unhandled error without all fields.
    # Ideally, your CardService would validate and return a 400.
    assert response.status_code == 400 # Or 400 if validation is in place


def test_get_all_cards(test_client, init_database, new_card_data):
    """
    GIVEN a Flask application configured for testing and cards exist in the database
    WHEN the '/api/cards' endpoint is requested (GET)
    THEN a list of cards should be returned with a 200 status code
    """
    # Add a card first
    test_client.post('/api/cards', content_type='multipart/form-data', data=new_card_data)

    response = test_client.get('/api/cards')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0
    assert response.json[0]['playerName'] == new_card_data['playerName']

def test_get_card_by_id_success(test_client, init_database, new_card_data):
    """
    GIVEN a Flask application configured for testing and a specific card exists
    WHEN the '/api/cards/<card_id>' endpoint is requested (GET) with an existing card ID
    THEN the card details should be returned with a 200 status code
    """
    post_response = test_client.post('/api/cards', content_type='multipart/form-data', data=new_card_data)
    card_id = post_response.json['id']

    response = test_client.get(f'/api/cards/{card_id}')
    assert response.status_code == 200
    assert response.json['id'] == card_id
    assert response.json['playerName'] == new_card_data['playerName']

def test_get_card_by_id_not_found(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/cards/<card_id>' endpoint is requested (GET) with a non-existent card ID
    THEN a 404 status code should be returned
    """
    response = test_client.get('/api/cards/9999') # Assuming 9999 does not exist
    assert response.status_code == 404
    assert response.json['message'] == 'Card not found'

def test_delete_card_success(test_client, init_database, new_card_data):
    """
    GIVEN a Flask application configured for testing and a specific card exists
    WHEN the '/api/cards/<card_id>' endpoint is requested (DELETE) with an existing card ID
    THEN the card should be deleted and a 204 status code returned
    """
    post_response = test_client.post('/api/cards', content_type='multipart/form-data', data=new_card_data)
    card_id = post_response.json['id']

    response = test_client.delete(f'/api/cards/{card_id}')
    assert response.status_code == 204 # No content for successful deletion
    
    # Verify card is deleted from DB
    deleted_card = Card.query.get(card_id)
    assert deleted_card is None
    
    # Optionally, verify that images are deleted from the filesystem if your service handles that.

def test_delete_card_not_found(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/cards/<card_id>' endpoint is requested (DELETE) with a non-existent card ID
    THEN a 404 status code should be returned
    """
    response = test_client.delete('/api/cards/9999') # Assuming 9999 does not exist
    assert response.status_code == 404
    assert response.json['message'] == 'Card not found'
