# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from dotenv import load_dotenv

# Import password hashing ONLY IF doing auto-admin creation in init
from werkzeug.security import generate_password_hash # <--- NEW import here

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()

def create_app():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    static_folder_path = os.path.join(project_root, 'static')
    
    app = Flask(__name__, instance_relative_config=True, static_folder=static_folder_path)

    load_dotenv()
    from config import Config
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    # Import blueprints AFTER extensions are initialized
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # <--- NEW: Automated Database Initialization and Admin Creation --->
    # This block will run when the app starts. It ensures migrations are applied
    # and an initial admin user is created IF the database is empty.
    # It will only run ONCE on a fresh database.
    with app.app_context():
        # Import models here to avoid circular imports at module level
        from app.models import User, LoginActivity
        
        # Apply database migrations
        # This command will check for new migrations and apply them.
        # It's safe to run multiple times; it only applies unapplied migrations.
        # Ensure 'flask_migrate' is installed.
        try:
            from flask.cli import current_app
            from flask_migrate import upgrade as db_upgrade # Import upgrade function
            print("Attempting to run database migrations...")
            db_upgrade() # Run all pending migrations
            print("Database migrations checked/applied.")
        except Exception as e:
            print(f"Error during database migration: {e}")
            # In production, you might want more robust error logging or alerting
            # but for a small app, this print is fine.

        # Create a default admin user if one doesn't already exist.
        # This is a simple way to ensure you always have an admin for initial access.
        default_admin_email = os.environ.get('DEFAULT_ADMIN_EMAIL') or 'admin@example.com' # Use env var or default
        default_admin_password = os.environ.get('DEFAULT_ADMIN_PASSWORD') or 'StrongPassword123!' # Use env var or default
        default_admin_username = os.environ.get('DEFAULT_ADMIN_USERNAME') or 'admin' # Use env var or default

        admin_user = User.query.filter_by(email=default_admin_email).first()
        if not admin_user:
            print(f"Creating default admin user: {default_admin_email}")
            hashed_password = generate_password_hash(default_admin_password)
            new_admin = User(
                username=default_admin_username,
                email=default_admin_email,
                password=hashed_password,
                is_admin=True
            )
            db.session.add(new_admin)
            try:
                db.session.commit()
                print("Default admin user created successfully.")
            except Exception as e:
                db.session.rollback()
                print(f"Error creating default admin user: {e}")
        else:
            print(f"Admin user '{default_admin_email}' already exists.")
    # <--- END NEW Section --->

    return app
