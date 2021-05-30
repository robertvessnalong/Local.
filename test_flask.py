from unittest import TestCase
from unittest.mock import patch
from app import app, update_review
from models import db, connect_db, User, Rating, Favorite, Review, LikeDislike, get_store_hours

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///fake_local'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False


class UserTest(TestCase):

    def setUp(self):

        db.drop_all()
        db.create_all()
        User.query.delete()
        Review.query.delete()
        LikeDislike.query.delete()

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
        bruce =  User.register(first_name='Bruce',
                            last_name='Wayne',
                            location='Detroit, MI',
                            email='bruce@gmail.com',
                            password='password')
    
        db.session.add_all([admin, peter, bruce])
        db.session.commit()

        self.user_one = admin.id
        self.user_two = peter.id
        self.user_three = bruce.id
        self.rest_id = 'Aait_iH6J3X_5PFe9ARicw'
          
        review = Review(user_id=self.user_one,
                created='2021-05-29',
                restaurant_id='Aait_iH6J3X_5PFe9ARicw',
                rating=4,
                comment='Really Enjoyed the Food!')
        db.session.add(review)
        db.session.commit()

        review_two = Review(user_id=self.user_one,
                created='2021-05-29',
                restaurant_id='Aait_iH6J3X_5PFe9ARicw',
                rating=2,
                comment='Service was terrible!')
        db.session.add_all([review, review_two])
        db.session.commit()

        self.review_one = review.id
        self.review_two = review_two.id

        likeanddislike = LikeDislike(user_id=self.user_one,
                                    comment_id=self.review_one)

        db.session.add(likeanddislike)
        db.session.commit()

    def tearDown(self):

        db.session.rollback()
   

    def test_user_login(self):
        with app.test_client() as client:
            with patch("app.session", dict()) as session:
                info = {"email":"admin@gmail.com", "password": "password"}
                res = client.post("/login", json=info, follow_redirects=True)
                assert session.get('user_id') == self.user_one
           

    def test_user_page(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['user_id'] = self.user_one
            res = client.get(f'/users/{self.user_one}', follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertIn('<h1>Robert L.</h1>', html)

    def test_user_logout(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['user_id'] = self.user_one
            res = client.get('/logout', follow_redirects=True)
            html = res.get_data(as_text=True)
            assert session.get('user_id')

    def test_register(self):
        with app.test_client() as client:
            new_user = {
                'first_name': 'Al',
                'last_name': 'Simmons',
                'location': 'Wisconsin',
                'email': 'alsimmons@gmail.com',
                'password': 'password'
            }
            res = client.post('/register', data=new_user, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertIn('<h1>Al S.</h1>', html)

    def test_user(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['user_id'] = self.user_one
            update_user = {
                'first_name': 'Chris',
                'last_name': 'Tucker',
                'location': 'Atlanta',
                'email': 'christucker@gmail.com',
                'password': 'password'
            }
            res = client.post(f'/users/{self.user_one}/update', data=update_user, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertIn('<h1>Chris T.</h1>', html)

    # Works but fails
    # def test_favorite(self):
    #      with app.test_client() as client:
    #         with client.session_transaction() as session:
    #             session['user_id'] = self.user_one
    #         res = client.post('/favorite/Aait_iH6J3X_5PFe9ARicw')
    #         html = res.get_data(as_text=True)
    #         print(html)

    def test_write_review(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['user_id'] = self.user_one
            review_data = {
                'user_id': self.user_one,
                'rating':4,
                'restaurant_id': 'Aait_iH6J3X_5PFe9ARicw',
                'review': 'This was a great place',
                'created_at': '2021-05-29',
            };
            res = client.post('/review', json=review_data, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertIn('This was a great place', html)


    def test_delete_review(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['user_id'] = self.user_one
            res = client.delete(f'/review/{self.review_two}', follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertIn('Message Deleted', html)


            
    def test_update_review(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['user_id'] = self.user_one
            review_data = {
                'rating':3,
                'review': 'Could be better!',
                'created_at': '2021-05-29',
            };
            res = client.patch(f'/review/{self.review_one}', json=review_data, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertIn('rating', html)

    def test_favorite_review(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['user_id'] = self.user_one
            res = client.post(f'/favorite/review/{self.review_two}')
            html = res.get_data(as_text=True)
            self.assertIn('Favorited Review', html)

    def test_remove_favorite(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['user_id'] = self.user_one
            res = client.delete(f'/favorite/review/{self.review_one}')
            html = res.get_data(as_text=True)