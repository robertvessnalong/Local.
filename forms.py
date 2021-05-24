from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Email, Length, NumberRange, Optional


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    location = StringField('Location', validators=[Optional()])
    email = StringField('Email Address', validators=[Email(), InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class UpdateUser(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    location = StringField('Location', validators=[Optional()])
    email = StringField('Email Address', validators=[Email(), InputRequired()])


class ReviewForm(FlaskForm):
    class Meta:
        csrf = False
    rating = IntegerField('Rating', validators=[InputRequired(), NumberRange(min=0, max=5)])
    review = StringField('Review', validators=[InputRequired(), Length(max=180)])
    restaurant_id = StringField('Restaurant ID', validators=[InputRequired()])

class EditReview(FlaskForm):
    class Meta:
        csrf = False
        rating = IntegerField('Rating', validators=[InputRequired(), NumberRange(min=0, max=5)])
        review = StringField('Review', validators=[InputRequired(), Length(max=180)])
