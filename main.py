#UPDATE FLASK REQUIREMENTS BEFORE COMMITING MAIN.PY to GITHUB,
#I DON'T THINK ANYTHING HAS CHANGED, BUT JUST BEING CAUTIOUS

import os
from flask import Flask, url_for, render_template, redirect, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user, logout_user#
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, SelectField
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

#Forms
#-----

class registerForm(FlaskForm):
    firstName = StringField('First Name:', validators=[InputRequired()])
    lastName = StringField('Last Name:', validators=[InputRequired()])
    email = StringField('Email:', validators=[InputRequired(), Email()])
    username = StringField('Username:', validators=[InputRequired()])
    password = PasswordField('Password:', validators=[InputRequired()])
    city = StringField('City:', validators=[InputRequired()])
    state = SelectField('Select State:', choices=[('Alabama'),('Louisiana')])
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


#Views
#-----
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registerForm()
    if form.validate_on_submit():
        test = True
        if test == True:
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
            return redirect(url_for('register'))
        
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
