from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Optional


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    location = StringField('Location', validators=[Optional()])
    email = StringField('Email Address', validators=[Email(), InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

