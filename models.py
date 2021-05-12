""" Models for Local. """

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import math
from datetime import date, datetime
import calendar

from sqlalchemy.orm import backref

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.location} {u.email}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)


    @classmethod
    def register(cls, first_name, last_name, location, email, password):
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        return cls(first_name = first_name, last_name = last_name, location=location, email=email, password=hashed_utf8)

    @classmethod
    def authenticate(cls, email, password):
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
        
    favorites = db.relationship('Favorite', backref="users")


class Rating(db.Model):

    __tablename__ ='ratings'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    restaurant_id = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False, default=0)

    @classmethod
    def convert_restaurant_rating(cls, rating):
        rating_data = {
        'number': 0,
        'isInt': False
    }
        if rating.is_integer():
            rating_data['number'] = int(rating)
            rating_data['isInt'] = True
            return rating_data
        else:
            rating_data['number'] = math.ceil(rating)
            rating_data['isInt'] = False
            return rating_data

class Favorite(db.Model):

    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    restaurant_id = db.Column(db.Text, nullable=False)

class Comment(db.Model):

    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    restaurant_id = db.Column(db.Text, nullable=False)
    comment = db.Column(db.String(180), nullable=False)

class LikeDislike(db.Model):

    __tablename__ = 'likeanddislike'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), primary_key=True)
    likeordislike = db.Column(db.Text)



def get_store_hours(store_hours):
    days = ['Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    data = {}
    if 'hours' in store_hours:
        data['is_open_now'] =  store_hours['hours'][0]['is_open_now']
        current_date = date.today()
        current_day = calendar.day_name[current_date.weekday()]
        for hours in store_hours['hours'][0]['open']:
            if hours['day'] == days.index(current_day):
                convert_time_start = datetime.strptime(hours['start'], "%H%M")
                formated_start = convert_time_start.strftime("%-I:%M %p")
                convert_time_end = datetime.strptime(hours['end'], "%H%M")
                formated_end = convert_time_end.strftime("%I:%M %p")
                data['start'] = formated_start
                data['end'] = formated_end 
                return data
   
            