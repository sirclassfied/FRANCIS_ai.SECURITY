# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager # Import LoginManager
from dotenv import load_dotenv

# Initialize extensions without linking to 'app' yet.
# These are the global instances that other modules (like models.py, routes.py) will import.
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager() # Initialize LoginManager instance

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Load environment variables from .env file (if it exists)
    load_dotenv()

    # Load configuration from config.py
    # Ensure 'config' module is importable (i.e., config.py is in your project root)
    from config import Config
    app.config.from_object(Config)

    # Initialize extensions with the app instance
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # Flask-Login Setup
    login_manager.init_app(app)
    # This specifies the endpoint (route function name) for the login page.
    # If a user tries to access a @login_required route but isn't logged in,
    # Flask-Login will redirect them here. 'main' is your blueprint name.
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info' # Category for flash messages

    @login_manager.user_loader
    def load_user(user_id):
        # This function tells Flask-Login how to load a user given their ID
        # It's crucial for keeping users logged in across requests.
        # Import User model here to avoid circular imports at top-level.
        from app.models import User
        return User.query.get(int(user_id))

    # Import blueprints HERE and register them AFTER extensions are initialized.
    # This prevents circular imports where blueprints/models might try to use 'db'
    # before it's fully set up with the app instance.
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app