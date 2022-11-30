
import os
from flask import Flask, url_for, render_template, redirect, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, SelectField, IntegerField, TextAreaField
from wtforms.validators import InputRequired, Email
from werkzeug.security import generate_password_hash, check_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = '1211109876543210ZyxwvutsrQponmlkjihgfedcbA'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///'+ os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

#Databases/Models
#----------------

class User(UserMixin, db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String)
    lastName = db.Column(db.String)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    isPersonalProfile = db.Column(db.Boolean, default=False, nullable=False)
    isStore = db.Column(db.Boolean, default=False, nullable=False)
    

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    storeName = db.Column(db.String)
    storeAddress = db.Column(db.String)
    storeCityName = db.Column(db.String(64))
    storeStateName = db.Column(db.String(64))
    storeZipCode = db.Column(db.Integer)
    storeManagerFullName = db.Column(db.String)
    storeEmail = db.Column(db.String(64), unique=True, index=True)
    storePhoneNumber = db.Column(db.String(24))
    games = db.Column(db.String)
    date = db.Column(db.String)
    time = db.Column(db.String)

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)

#Forms
#-----

class registerForm(FlaskForm):
    firstName = StringField('First Name:', validators=[InputRequired()])
    lastName = StringField('Last Name:', validators=[InputRequired()])
    email = StringField('Email:', validators=[InputRequired(), Email()])
    username = StringField('Username:', validators=[InputRequired()])
    password = PasswordField('Password:', validators=[InputRequired()])
    city = StringField('City:', validators=[InputRequired()])
    state = SelectField('Select State:', choices=[('Alabama'),('Alaska'),
                                                  ('Arizona'),('Arkansas'),
                                                  ('California'),('Colorado'),
                                                  ('Connecticut'), ('Delaware'),
                                                  ('Florida'), ('Georgia'),
                                                  ('Hawaii'), ('Idaho'),
                                                  ('Illinois'), ('Indiana'),
                                                  ('Iowa'), ('Kansas'),
                                                  ('Kentucky'), ('Louisiana'),
                                                  ('Maine'), ('Maryland'),
                                                  ('Massachusetts'),('Michigan'),
                                                  ('Minnesota'), ('Mississippi'),
                                                  ('Missouri'), ('Montana'),
                                                  ('Nebraska'), ('Nevada'),
                                                  ('New Hampshire'), ('New Jersey'),
                                                  ('New Mexico'), ('New York'),
                                                  ('North Carolina'), ('North Dakota'),
                                                  ('Ohio'), ('Oklahoma'),
                                                  ('Oregon'), ('Pennsylvania'),
                                                  ('Rhode Island'), ('South Carolina'),
                                                  ('South Dakota'), ('Tennessee'),
                                                  ('Texas'), ('Utah'),
                                                  ('Vermont'), ('Virginia'),
                                                  ('Washington'), ('West Virginia'),
                                                  ('Wisconsin'), ('Wyoming')])
    isPersonalProfile = BooleanField('Personal Profile', default=False)
    isStore = BooleanField('Store Profile', default=False)
    submit = SubmitField('Submit')
     #These conditionals are set with a query of the first item that matches the
    #provided username in the User database/model. If anything matches the provided
    #username, then raise a ValidationError, because that username
    #already exists/has been registered already.
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

        #Update User information.
class UpdateForm(FlaskForm): 
    firstName = StringField('First Name:', validators=[InputRequired()])
    lastName = StringField('Last Name:', validators=[InputRequired()])
    email = StringField('Email:', validators=[InputRequired(), Email()])
    username = StringField('Username:', validators=[InputRequired()])
    submit = SubmitField('Update')
    #These conditionals are set with a query of the first item that matches the
    #provided username in the User database/model. If anything matches the provided
    #username, then raise a ValidationError, because that username
    #already exists/has been registered already.
    def validate_username(self, field):
        if username.data != current_user.username:
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('Username already in use.')

class loginForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired()])
    password = PasswordField('Password:', validators=[InputRequired()])
    submit = SubmitField('Login')

    def validate_username(self, field):

        #This is set with a query of the first item that matches the provided username in the User database/model.
        if User.query.filter_by(username=field.data).first():
            # do nothing/ this username is valid because it has already been registered

            # had to print something here, otherwise this error persists: "IndentationError: expected an indented block after 'if' statement on line ###"
            print('something')

        #After a query, if there is no first item that matches the provided username in the User database/model,
        #then that means the provided username has not been registered, so raise an error
        else:
            raise ValidationError('That username does not exist. If you have yet to register, then please do so to login.')
        
class hostEventForm(FlaskForm):
    storeName = StringField('Store name:', validators=[InputRequired()])
    storeAddress = StringField('Store address:', validators=[InputRequired()])
    storeCityName = StringField("Store's city:", validators=[InputRequired()])
    storeStateName = SelectField("Store's state:", choices=[('Alabama'),('Alaska'),
                                                  ('Arizona'),('Arkansas'),
                                                  ('California'),('Colorado'),
                                                  ('Connecticut'), ('Delaware'),
                                                  ('Florida'), ('Georgia'),
                                                  ('Hawaii'), ('Idaho'),
                                                  ('Illinois'), ('Indiana'),
                                                  ('Iowa'), ('Kansas'),
                                                  ('Kentucky'), ('Louisiana'),
                                                  ('Maine'), ('Maryland'),
                                                  ('Massachusetts'),('Michigan'),
                                                  ('Minnesota'), ('Mississippi'),
                                                  ('Missouri'), ('Montana'),
                                                  ('Nebraska'), ('Nevada'),
                                                  ('New Hampshire'), ('New Jersey'),
                                                  ('New Mexico'), ('New York'),
                                                  ('North Carolina'), ('North Dakota'),
                                                  ('Ohio'), ('Oklahoma'),
                                                  ('Oregon'), ('Pennsylvania'),
                                                  ('Rhode Island'), ('South Carolina'),
                                                  ('South Dakota'), ('Tennessee'),
                                                  ('Texas'), ('Utah'),
                                                  ('Vermont'), ('Virginia'),
                                                  ('Washington'), ('West Virginia'),
                                                  ('Wisconsin'), ('Wyoming')])
    storeZipCode = IntegerField('Store zip code:', validators=[InputRequired()])
    storeManagerFullName = StringField('Store manager full name:', validators=[InputRequired()])
    storeEmail = StringField('Store email:', validators=[InputRequired(), Email()])
    storePhoneNumber = StringField("Store's phone number:", validators=[InputRequired()])
    games = StringField('Game(s):', validators=[InputRequired()])
    date = StringField('Date:', validators=[InputRequired()])
    time = StringField('Time:', validators=[InputRequired()])
    submit = SubmitField('Submit')

class joinEventForm(FlaskForm):
    content = TextAreaField("Tell everyone that you're going to this event!: ")
    submit = SubmitField('Submit')
    

#LoginManager
#------------
#Configure the login manager so that it knows how to identify a user.
#It is important to provide a user loader callback when using Flask-Login.
#This keeps the current user object loaded in that current session based on the stored id.

login_manager = LoginManager(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
            


#Views
#-----
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registerForm()
    if form.validate_on_submit():
        db.session.add(User(firstName = form.firstName.data, lastName = form.lastName.data, email = form.email.data, username = form.username.data,
                            password = form.password.data, city = form.city.data, state = form.state.data, isPersonalProfile = form.isPersonalProfile.data,
                            isStore = form.isStore.data))
        db.session.commit()
        form.firstName.data = ''
        form.lastName.data = ''
        form.email.data = ''
        form.username.data = ''
        form.password.data = ''
        form.city.data = ''
        form.state.data = ''
        form.isPersonalProfile.data = ''
        form.isStore.data = ''
        return redirect(url_for('login'))
        
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():

        #The userName variable below is set with a query of the first item that matches the provided username in the User database/model
        userName = User.query.filter_by(username=form.username.data).first()

        #If the provided username exists in the User table and the password associated with that username is verifiable
        #then log the user in and redirect/refresh to login.html:
        if userName is not None and userName.verify_password(form.password.data):
            login_user(userName)
            return redirect(url_for('profile'))
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    #logout the current user
    logout_user()
    return redirect(url_for('login'))

@app.route('/hostEvent', methods=['GET','POST'])
@login_required
def hostEvent():
    form = hostEventForm()
    if form.validate_on_submit():
        db.session.add(Event(storeName = form.storeName.data,
                             storeAddress = form.storeAddress.data,
                             storeCityName = form.storeCityName.data,
                             storeStateName = form.storeStateName.data,
                             storeZipCode = form.storeZipCode.data,
                             storeManagerFullName = form.storeManagerFullName.data,
                             storeEmail = form.storeEmail.data,
                             storePhoneNumber = form.storePhoneNumber.data,
                             games = form.games.data,
                             date = form.date.data,
                             time = form.time.data))
        db.session.commit()
        form.storeName.data = ''
        form.storeAddress.data = ''
        form.storeCityName.data = ''
        form.storeStateName.data = ''
        form.storeZipCode.data = ''
        form.storeManagerFullName.data = ''
        form.storeEmail.data = ''
        form.storePhoneNumber.data = ''
        form.games.data = ''
        form.date.data = ''
        form.time.data = ''
        return redirect(url_for('hostEvent'))
    return render_template('hostEvent.html', form=form)

@app.route('/joinEvent', methods=['GET', 'POST'])
@login_required
def joinEvent():
    form = joinEventForm()
    if form.validate_on_submit():
        db.session.add(Message(content = form.content.data))
        db.session.commit()
        form.content.data=''
        return redirect(url_for('joinEvent'))
    messageTable = Message.query.all()
    eventsTable = Event.query.all()
    return render_template('joinEvent.html', eventsTable=eventsTable, messageTable=messageTable, form=form)

@app.route('/error401', methods=['GET', 'POST'])
def error401():
    return render_template('error401.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
     
    return render_template('profile.html')

if __name__ == "__main__":
    app.run(debug=True)

