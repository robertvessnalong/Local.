
from flask import Flask, render_template, redirect, flash, session, jsonify, request
from models import db, connect_db, User, Rating, Favorite, Comment, LikeDislike
from forms import RegisterForm, LoginForm, UpdateUser
from ipstack import GeoLookup
from config import yelp_api_key, ipstack
import json
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///local'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'helloworld'
geo_lookup = GeoLookup(ipstack)
location_data = geo_lookup.get_own_location()

connect_db(app)
db.create_all()

headers = {'Authorization': 'Bearer %s' % yelp_api_key}
url_search = "https://api.yelp.com/v3/businesses/search"
url_single = "https://api.yelp.com/v3/businesses/"



@app.route('/')
def homepage():
        # new_restaurants = {'categories': 'restaurants',
        #                    'location': 'Roseville, MI',
        #                 #    'latitude': location_data['latitude'], 
        #                 #    'longitude': location_data['longitude'], 
        #                    'attributes': 'hot_and_new',
        #                    'limit': 6}
        # restaurant_request =requests.get(url_search, params=new_restaurants, headers=headers)
        # data = restaurant_request.json()
        # return render_template('homepage.j2', rest=data['businesses'])
        return render_template('homepage.j2')
        
    

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        f_name = form.first_name.data
        l_name = form.last_name.data
        location = form.location.data
        email = form.email.data
        password = form.password.data
        register_user = User.register(f_name,
                                      l_name,
                                      location or location_data['city'],
                                      email,
                                      password)
        db.session.add(register_user)
        db.session.commit()
        session['user_id'] = register_user.id
        return redirect('/')
    return render_template('register.j2', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.authenticate(email, password)
        if user:
            session['user_id'] = user.id
            return redirect('/')
        else:
            form.email.errors = ['Invalid username/password.']
    return render_template('login.j2', form=form)

@app.route('/users/<user_id>')
def user_page(user_id):
    if "user_id" not in session:
        return redirect('/')
    user = User.query.get_or_404(user_id)
    if user.id == session['user_id']:
        return render_template('user.j2', user=user)
    else:
        return redirect('/')
    

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


@app.route('/users/<int:user_id>/update', methods=["GET", "POST"])
def update_user(user_id):
    if "user_id" not in session:
        return redirect('/login')
    user = User.query.get_or_404(user_id)
    form = UpdateUser(obj=user)
    if user.id == session['user_id']:
        if form.validate_on_submit():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.location = form.location.data
            user.email = form.email.data
            db.session.add(user)
            db.session.commit()
            return redirect(f'/users/{user_id}')
        return render_template('edit_user.j2', form=form, user=user)
    else:
        return redirect('/login')
    


@app.route('/restaurant/<rest_id>')
def restaurant_page(rest_id):
    # single_restaurant_url = url_single + f"{rest_id}" 
    # single_rest_request = requests.get(single_restaurant_url,  headers=headers)
    
    data = {
    "id": "gR9DTbKCvezQlqvD7_FzPw",
    "alias": "north-india-restaurant-san-francisco",
    "name": "North India Restaurant",
    "image_url": "https://s3-media4.fl.yelpcdn.com/bphoto/8713LkYA3USvWj9z4Yokjw/o.jpg",
    "is_claimed": True,
    "is_closed": False,
    "url": "https://www.yelp.com/biz/north-india-restaurant-san-francisco?adjust_creative=srFoJHnY-90t-yQ13y0aEw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_lookup&utm_source=srFoJHnY-90t-yQ13y0aEw",
    "phone": "+14153481234",
    "display_phone": "(415) 348-1234",
    "review_count": 1779,
    "categories": [
        {
            "alias": "indpak",
            "title": "Indian"
        }
    ],
    "rating": 4.0,
    "location": {
        "address1": "123 Second St",
        "address2": "",
        "address3": "",
        "city": "San Francisco",
        "zip_code": "94105",
        "country": "US",
        "state": "CA",
        "display_address": [
            "123 Second St",
            "San Francisco, CA 94105"
        ],
        "cross_streets": ""
    },
    "coordinates": {
        "latitude": 37.787789124691,
        "longitude": -122.399305736113
    },
    "photos": [
        "https://s3-media4.fl.yelpcdn.com/bphoto/8713LkYA3USvWj9z4Yokjw/o.jpg",
        "https://s3-media4.fl.yelpcdn.com/bphoto/W2oBBWPGm3bRYEuHKGMtCw/o.jpg",
        "https://s3-media1.fl.yelpcdn.com/bphoto/YrS539sVhmyOZcowdJsP_Q/o.jpg"
    ],
    "price": "$$",
    "hours": [
        {
            "open": [
                {
                    "is_overnight": False,
                    "start": "1000",
                    "end": "2300",
                    "day": 0
                },
                {
                    "is_overnight": False,
                    "start": "1000",
                    "end": "2300",
                    "day": 1
                },
                {
                    "is_overnight": False,
                    "start": "1000",
                    "end": "2300",
                    "day": 2
                },
                {
                    "is_overnight": False,
                    "start": "1000",
                    "end": "2300",
                    "day": 3
                },
                {
                    "is_overnight": False,
                    "start": "1000",
                    "end": "2330",
                    "day": 4
                },
                {
                    "is_overnight": False,
                    "start": "1000",
                    "end": "2330",
                    "day": 5
                },
                {
                    "is_overnight": False,
                    "start": "1000",
                    "end": "2300",
                    "day": 6
                }
            ],
            "hours_type": "REGULAR",
            "is_open_now": True
        }
    ],
    "transactions": [
        "pickup",
        "delivery",
        "restaurant_reservation"
    ]
}
    rating = Rating.convert_restaurant_rating(data['rating'])
    return render_template('restaurant_page.j2', rest=data, rating=rating)

