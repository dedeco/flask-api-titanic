from flask_sqlalchemy import SQLAlchemy

from .app import app

db = SQLAlchemy(app)
db.init_app(app)

class Passenger(db.Model):
    __tablename__ = 'passengers'
    
    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])
        self.ChangeToSurvive = round(self.ChangeToSurvive, 1)

    def dict(self):
        x = self.__dict__
        if x:
            del x['_sa_instance_state'] 
        return x

    PassengerId = db.Column(db.Integer,primary_key=True)
    Name = db.Column(db.String(255))
    Sex = db.Column(db.String(32))
    Age = db.Column(db.Integer)
    SibSp = db.Column(db.Integer)
    Parch = db.Column(db.Integer)
    Embarked = db.Column(db.String(1))
    Survived = db.Column(db.Integer)
    ChangeToSurvive = db.Column(db.Float)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)