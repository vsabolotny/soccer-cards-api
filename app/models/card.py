from .. import db # Import the db instance from app/__init__.py
from datetime import datetime

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(100), nullable=False)
    card_year = db.Column(db.Integer, nullable=False)
    team = db.Column(db.String(100), nullable=False)
    image_front_url = db.Column(db.String(200), nullable=False)
    image_back_url = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # Add any other fields you need, e.g., user_id if cards are linked to users
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Card {self.id} - {self.player_name}>"

    def to_dict(self):
        return {
            'id': self.id,
            'playerName': self.player_name,
            'cardYear': self.card_year,
            'team': self.team,
            'imageFrontUrl': self.image_front_url,
            'imageBackUrl': self.image_back_url,
            'dateAdded': self.date_added.isoformat() if self.date_added else None
        }