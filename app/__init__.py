from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .email_alerts import configure_mail

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    configure_mail(app)

    from .routes import main
    app.register_blueprint(main)

    return app