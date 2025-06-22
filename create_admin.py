# create_admin.py
# Import the app factory and db instance from your core app package
from app import create_app, db
from app.models import User # Corrected import path for models

from werkzeug.security import generate_password_hash # For password hashing

def create_admin_user():
    # Create an app instance using the factory
    app = create_app()

    # Establish an application context using the created app instance
    with app.app_context():
        print("--- Create Admin User ---")
        username = input("Enter admin username: ")
        email = input("Enter admin email: ")
        password = input("Enter admin password: ")

        if not username or not email or not password:
            print("Error: All fields (username, email, password) are required.")
            return

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"Error: User with email '{email}' already exists. Please use a different email.")
            return

        hashed_password = generate_password_hash(password)
        new_admin = User(username=username, email=email, password=hashed_password, is_admin=True)

        try:
            db.session.add(new_admin)
            db.session.commit()
            print(f"\nAdmin user '{username}' with email '{email}' created successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred while creating the user: {e}")

if __name__ == '__main__':
    create_admin_user()