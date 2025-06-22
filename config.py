# config.py
import os

class Config:
    # Use os.environ.get to fetch from environment variables (recommended for deployment)
    # Provide a strong fallback or ensure .env is correctly loaded.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'francislota08_super_secure_key'

    # Database configuration
    # For SQLite, it's relative to the instance folder
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///instance/site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Recommended: silence Flask-SQLAlchemy warnings

    # Flask-Mail configuration
    # Ensure these are set in your .env file in production
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.googlemail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('francislota08@gmail') # Your email for sending
    MAIL_PASSWORD = os.environ.get('quitsgfjavbunkgx') # Your email password/app password
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'francislota08@gmail' # Email from which alerts/resets are sent