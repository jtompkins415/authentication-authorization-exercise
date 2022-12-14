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
    

    @classmethod
    def register(cls,username,pwd,email,first_name,last_name):
        '''Register user and hash user's password'''

        hash = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hash.decode('utf8')

        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    
    @classmethod
    def authenticate(cls,username,pwd):
        '''Authenticate user'''

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False
    

class Feedback(db.Model):
    '''Feedback class'''

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.VARCHAR(length=100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.VARCHAR(length=20), db.ForeignKey('users.username'))

    user = db.relationship('User', backref = 'feedback')

    def __repr__(self):
        return f'<Feedback id={self.id} title={self.title} username={self.username}>'
    
    

