# run.py

# ONLY import the create_app factory function from your 'app' package
from app import create_app

# Call the factory function to create and configure your Flask application instance
app = create_app()

# This block ensures the development server only runs when run.py is executed directly
if __name__ == '__main__':
    # Use app.config.get() for robustness, or directly app.config['FLASK_ENV']
    # Ensure FLASK_ENV is set in your .env or config.py for 'development'
    # Example .env: FLASK_ENV=development
    app.run(debug=app.config.get('FLASK_ENV') == 'development')