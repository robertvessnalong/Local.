from unittest import TestCase
from unittest.mock import patch

from app import app
from models import db, connect_db, User, Rating, Favorite, Review, LikeDislike, get_store_hours

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///fake_local'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()

class UserTest(TestCase):

    def setUp(self):

        User.query.delete()

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
                session['user_id'] = 4
            res = client.get('/logout', follow_redirects=True)
            html = res.get_data(as_text=True)
            assert session.get('user_id')

    def test_register(self):
        with app.test_client() as client:
            new_user = {
                'first_name': 'Al',
                'last_name': 'Simmons',
                'location': 'Wisconsin',
                'email': 'al@gmail.com',
                'password': 'password'
            }
            res = client.post('/register', new_user, follow_redirects=True)
            html = res.get_data(as_text=True)
            print(html)