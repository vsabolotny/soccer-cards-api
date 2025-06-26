from flask import jsonify
from ..models.card import Card
from .. import db  # Assuming db is initialized in app/__init__.py
print(f"ID of db in card_service.py (after import): {id(db)}")  # DIAGNOSTIC
import os
from werkzeug.utils import secure_filename

# Define UPLOAD_FOLDER relative to the 'app' package directory
# os.path.dirname(__file__) is the 'services' directory (e.g., backend/app/services)
# os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) is the 'app' directory (e.g., backend/app)
APP_PACKAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOAD_FOLDER = os.path.join(APP_PACKAGE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class CardService:
    def __init__(self):
        # This self.cards list seems unused if you are using SQLAlchemy (Card.query, db.session)
        # You might want to remove it if it's a leftover from a previous implementation.
        self.cards = []

    def add_card(self, data, image_front, image_back):
        print(f"ID of db in card_service.add_card (at method start): {id(db)}")  # DIAGNOSTIC
        player_name = data.get('playerName')
        card_year = data.get('cardYear')
        team = data.get('team')

        if not all([player_name, card_year, team, image_front, image_back]):
            return {"error": "Missing data"}, 400

        if not (allowed_file(image_front.filename) and allowed_file(image_back.filename)):
            return {"error": "Invalid file type"}, 400

        # Ensure the upload folder exists
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        filename_front = secure_filename(image_front.filename)
        filename_back = secure_filename(image_back.filename)

        path_front = os.path.join(UPLOAD_FOLDER, filename_front)
        path_back = os.path.join(UPLOAD_FOLDER, filename_back)

        image_front.save(path_front)
        image_back.save(path_back)

        new_card = Card(
            player_name=player_name,
            card_year=int(card_year),  # Assuming card_year should be an integer
            team=team,
            image_front_url=f'/static/uploads/{filename_front}',  # URL to access the image
            image_back_url=f'/static/uploads/{filename_back}'  # URL to access the image
        )
        db.session.add(new_card)
        db.session.commit()
        return new_card.to_dict()  # Assuming Card model has to_dict()

    def get_all_cards(self, filters=None):
        query = Card.query
        if filters:
            player_name = filters.get('playerName')
            date_str = filters.get('date')
            if player_name:
                query = query.filter(Card.player_name.ilike(f"%{player_name}%"))
            # Add more filters as needed, e.g., for date
            # if date_str:
            #     try:
            #         date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            #         query = query.filter(Card.date_added == date_obj)  # Assuming Card model has date_added
            #     except ValueError:
            #         pass  # Handle invalid date format
        cards = query.all()
        return [card.to_dict() for card in cards]  # Assuming Card model has to_dict()

    def filter_cards(self, name=None, date=None):
        filtered_cards = self.cards
        if name:
            filtered_cards = [card for card in filtered_cards if name.lower() in card.name.lower()]
        if date:
            filtered_cards = [card for card in filtered_cards if card.date == date]
        return filtered_cards

    def get_card_by_id(self, card_id):
        card = Card.query.get(card_id)
        return card.to_dict() if card else None

    def delete_card(self, card_id):
        card = Card.query.get(card_id)
        if card:
            # Optionally, delete image files from server
            # if card.image_front_url:
            #     try:
            #         os.remove(os.path.join('app', card.image_front_url.lstrip('/')))
            #     except OSError:
            #         pass  # Handle file not found or other errors
            # if card.image_back_url:
            #     try:
            #         os.remove(os.path.join('app', card.image_back_url.lstrip('/')))
            #     except OSError:
            #         pass
            db.session.delete(card)
            db.session.commit()
            return True
        return False