from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

from app.user.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators= [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('sign up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators= [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')