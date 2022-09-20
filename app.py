from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import LoginForm, UserRegistration, FeedbackForm


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

# ------------------USER ROUTES--------------------


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
        return redirect(f'/users/{new_user.username}')
    
    return render_template('register.html', form=form) 

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    '''Show user login form and handle form submission'''

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f'Welcome back, {user.username}')
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password']

    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout_user():
    '''Logout user and remove themn from the session'''

    session.pop('username')
    return redirect('/')

@app.route('/users/<username>', methods=['GET'])
def user_details(username):
    '''Show details about logged in User'''
    user = User.query.get_or_404(username)

    if user.username != session['username']:
        flash('Login Required')
        return redirect('/login')
    else:
        feedback = Feedback.query.all()
        
        return render_template('user_detail.html', user=user, feedback=feedback)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    '''Delete User'''
    user = User.query.get_or_404(username)

    if user.username != session['username']:
        
        flash('Login Required')
        return redirect('/login')
    else:
        db.session.delete(user)
        db.session.commit()

        return redirect('/')

# -----------------FEEDBACK ROUTES-------------------

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    '''Show feedback form and handle form submission'''

    if 'username' not in session:
        flash('Login Required')
        return redirect('/login')
    
    form = FeedbackForm()

    if form.validate_on_submit():
        user = User.query.get_or_404(username)
        
        title = form.title.data
        content = form.content.data
        username = user.username

        new_feedback = Feedback(title=title, content=content, username=username)

        db.session.add(new_feedback)
        db.session.commit()

        return redirect(f'/users/{user.username}')
    else:
        return render_template('feedback_form.html', form=form)

@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    '''Update feedback and handle form submission'''
    
    feedback = Feedback.query.get_or_404(feedback_id)

    if feedback.user.username != session['username']:
        flash('Access Denied')
        return redirect('/login')
    
    form = FeedbackForm()
    
   
    if form.validate_on_submit():
        
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.add(feedback)
        db.session.commit()

        return redirect(f'/users/{feedback.user.username}')
    else:
        return render_template('update_feedback.html', form=form, feedback=feedback)

@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    '''Delete posted feedback'''

    feedback = Feedback.query.get_or_404(feedback_id)

    if session['username'] == feedback.user.username:
        flash('Access Denied')
        redirect('/login')

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f'/users/{feedback.user.username}')



