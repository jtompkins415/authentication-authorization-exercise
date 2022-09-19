from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    '''Connect to DB'''
   
    db.app = app
    db.init_app(app)
    

class User(db.Model):
    '''User class'''

    __tablename__ = 'users'

    username = db.Column(db.VARCHAR(length=20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.VARCHAR(length=50), nullable=False)
    first_name = db.Column(db.VARCHAR(length=30), nullable=False)
    last_name = db.Column(db.VARCHAR(length=30), nullable=False)

    def __repr__(self):
        return f'<User username={self.username} first_name={self.first_name} last_name={self.last_name}>'
    


