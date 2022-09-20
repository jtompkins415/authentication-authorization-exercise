from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import UserRegistration


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'Fe3dback123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/', methods=['GET'])
def redirect_to_register():
    '''Redirect to registartion page'''

    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    '''Show form for user registration and handle form submission'''

    form = UserRegistration()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()

        flash('User Created!')
        return redirect('/secret')
    
    return render_template('register.html', form=form) 

@app.route('/secret')
def congrats_message():

    return render_template('secret.html')