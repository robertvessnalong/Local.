""" Models for Local. """

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

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
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)


    @classmethod
    def register(cls, first_name, last_name, location, email, password):
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        return cls(first_name = first_name, last_name = last_name, location=location, email=email, password=hashed_utf8)


class Rating(db.Model):

    __tablename__ ='ratings'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    restaurant_id = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False, default=0)

class Favorite(db.Model):

    __tablename__ = 'favorites'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
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

