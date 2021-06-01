
import os
from unittest import TestCase
from sqlalchemy import exc 

from models import db, connect_db, User, Rating, Favorite, Review, LikeDislike

os.environ['DATABASE_URL'] = "postgresql:///fake_local"

from app import app

db.create_all()

class UserModelTestCase(TestCase):

    def setUp(self):

        db.drop_all()
        db.create_all()

        admin =  User.register(first_name='Robert',
                       last_name='Long',
                       location='Detroit, MI',
                       email='admin@gmail.com',
                       password='password')
        admin_id = 11
        admin.id = admin_id

        peter =  User.register(first_name='Peter',
                            last_name='Parker',
                            location='New York',
                            email='peter@gmail.com',
                            password='password')

        peter_id = 12
        peter.id = peter_id

        db.session.add_all([admin, peter])
        db.session.commit()

        u1 = User.query.get(admin_id)
        u2 = User.query.get(peter_id)
        
        self.u1 = u1
        self.uid1 = admin_id

        self.u2 = u2
        self.uid2 = peter_id

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):

        u = User(first_name='first_test',
                last_name='last_test',
                location='Detroit',
                email='test@gmail.com',
                password='HASHED_PASSWORD')

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.favorites), 0)
        self.assertEqual(len(u.reviewed), 0)

    def test_user_review(self):
        
        new_review = Review(user_id=self.uid1,
                created='2021-05-29',
                restaurant_id='Aait_iH6J3X_5PFe9ARicw',
                rating=4,
                comment='Really Enjoyed the Food!')

        self.u1.reviewed.append(new_review)
        db.session.commit()

        self.assertEqual(len(self.u1.reviewed), 1)

    def test_user_favorite(self):

        favorite = Favorite(user_id=self.uid1,
            restaurant_id='Aait_iH6J3X_5PFe9ARicw',
            name=self.u1.first_name,
            image_url= 'https://www.google.com',
            category='Fast Food')
        
        self.u1.favorites.append(favorite)
        db.session.commit()

        self.assertEqual(len(self.u1.favorites), 1)

    def test_user_likeordislike(self):

            new_review = Review(user_id=self.uid1,
                created='2021-05-29',
                restaurant_id='Aait_iH6J3X_5PFe9ARicw',
                rating=4,
                comment='Really Enjoyed the Food!')

            self.u1.reviewed.append(new_review)
            db.session.commit()

            like = LikeDislike(user_id=self.uid2,
                               comment_id=new_review.id)
            
            self.u2.liked.append(like)
            db.session.commit()

            self.assertEqual(len(self.u2.liked), 1)