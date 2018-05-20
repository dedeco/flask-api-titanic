from flask import Flask
from config import TRACK_MODIFICATIONS, DATABASE_URI

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = 'SECRET'
    return app

app = create_app()
