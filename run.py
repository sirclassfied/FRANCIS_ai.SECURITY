from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('config')  # or load config manually

db = SQLAlchemy(app)
mail = Mail(app)

# Register blueprints
from app.routes import main  # adjust import as needed
app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)
