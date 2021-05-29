""" Models for Local. """

from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import math
from datetime import date, datetime
import calendar
import os 

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
    reviewed = db.relationship('Review', backref="users")
    liked = db.relationship('LikeDislike', backref="users")


class Rating(db.Model):

    __tablename__ ='ratings'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    restaurant_id = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False, default=0)

    @classmethod
    def convert_restaurant_rating(cls, rating):
        rating_data = {
        'number': 0,
        'isInt': False,
        'image': ''
    }
        if rating["rating"].is_integer():
            rating_data['number'] = int(rating["rating"])
            rating_data['isInt'] = True
            rating_data['image'] = f'small_{int(rating["rating"])}@2x.png'
            return rating_data
        else:
            rating_data['number'] = math.ceil(rating['rating'])
            rating_data['isInt'] = False
            rating_data['image'] = f'small_{int(rating["rating"])}_half@2x.png'
            return rating_data

class Favorite(db.Model):

    __tablename__ = 'favorites'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    restaurant_id = db.Column(db.Text, nullable=False, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text)
    category = db.Column(db.Text)


    def serialize(self):
        return {
            'user_id': self.user_id,
            'restaurant_id': self.restaurant_id,
            'name': self.name,
            'image_url': self.image_url,
            'category': self.category
        }
        
class Review(db.Model):

    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    created = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    restaurant_id = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(180), nullable=False)


class LikeDislike(db.Model):

    __tablename__ = 'likeanddislike'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), primary_key=True)

    


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
   
            
# def get_rating_image(rating_data):
#     data = {
#         'image': ''
#     }
#         if rating_data['isInt'] == True:
#             if f'{rating_data["number"]}@' in filename:
#                 data['image'] = filename
#                 print(data)
#         else:
#            print('Hello World')
#     return rating_data