from models import db, connect_db, User, Rating, Favorite, Review, LikeDislike, get_store_hours
from app import app
import datetime

# Create All Tables
db.drop_all()
db.create_all()

User.query.delete()
Rating.query.delete()
Favorite.query.delete()
Review.query.delete()
LikeDislike.query.delete()

#Add Sample Users
admin =  User.register(first_name='Robert',
                       last_name='Long',
                       location='Detroit, MI',
                       email='admin@gmail.com',
                       password='password')
peter =  User.register(first_name='Peter',
                       last_name='Parker',
                       location='New York',
                       email='peter@gmail.com',
                       password='password')

db.session.add_all([admin, peter])
db.session.commit() 

#Add Sample Posts
apost =  Review(user_id=1,
                restaurant_id = 'qjU0VlJE7QKYgkuZIgAVKw',
                rating=4,
                comment='I will be coming back!',
                created=datetime.datetime.utcnow())
ppost =  Review(user_id=2,
                restaurant_id = 'qjU0VlJE7QKYgkuZIgAVKw',
                rating=3,
                comment='Food was ok!',
                created=datetime.datetime.utcnow())

db.session.add_all([apost, ppost])
db.session.commit()                     