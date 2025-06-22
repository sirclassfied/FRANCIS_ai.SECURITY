# app/models.py
from app import db # CORRECT: Import the db instance from your app package's __init__.py
from datetime import datetime
from flask_login import UserMixin # Needed for Flask-Login
from itsdangerous import TimedSerializer as Serializer # For secure, time-limited tokens
from flask import current_app # To access SECRET_KEY from app config

class User(db.Model, UserMixin): # Inherit from UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False) # For hashed passwords
    is_admin = db.Column(db.Boolean, default=False) # is_admin column

    def __repr__(self):
        return f'<User {self.username}>'

    # Method to generate a password reset token
    def get_reset_token(self, expires_sec=1800): # Token valid for 30 minutes (1800 seconds)
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # Static method to verify a password reset token
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None # Token is invalid or expired
        return User.query.get(user_id)


class LoginActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    ip_address = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_suspicious = db.Column(db.Boolean, default=False)