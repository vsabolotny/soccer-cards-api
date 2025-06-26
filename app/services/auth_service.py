from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db

class AuthService:
    @staticmethod
    def register_user(email, password):
        if User.query.filter_by(email=email).first():
            return False  # User already exists
        
        # Let Werkzeug use its default, more secure hashing method
        hashed_password = generate_password_hash(password) 
        
        new_user = User(email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return True

    @staticmethod
    def authenticate_user(email, password):
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            return user
        return None