
from flask import Flask, render_template, redirect, flash, session, jsonify, request
from models import db, connect_db, User, Rating, Favorite, Comment, LikeDislike, get_store_hours
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
        new_restaurants = {'categories': 'restaurants',
                           'latitude': location_data['latitude'], 
                           'longitude': location_data['longitude'], 
                           'attributes': 'hot_and_new',
                           'limit': 10}
        restaurant_request =requests.get(url_search, params=new_restaurants, headers=headers)
        data = restaurant_request.json()
        return render_template('homepage.j2', rest=data['businesses'])
        
    

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
    single_restaurant_url = url_single + f"{rest_id}" 
    single_rest_request = requests.get(single_restaurant_url,  headers=headers).json()
    rating = Rating.convert_restaurant_rating(single_rest_request['rating'])
    user = User.query.get_or_404(session['user_id'])
    user_favorites = Favorite.query.filter(Favorite.user_id == user.id).all()
    favorite = [favorite for favorite in user_favorites if favorite.restaurant_id == rest_id]
    time = get_store_hours(single_rest_request)
    return render_template('restaurant_page.j2', rest=single_rest_request, rating=rating, time=time, favorites=favorite)


@app.route('/favorite/<rest_id>')
def favorite_restaurant(rest_id):
    if "user_id" not in session:
        return redirect('/login')
    user = User.query.get_or_404(session['user_id'])
    favorite = Favorite(user_id = user.id, restaurant_id = rest_id)
    db.session.add(favorite)
    db.session.commit()
    return redirect(f'/restaurant/{rest_id}')


@app.route('/favorite/<rest_id>/remove')
def remove_favorite(rest_id):
    if "user_id" not in session:
        return redirect('/login')
    favorite_restaurant = Favorite.query.filter(Favorite.restaurant_id == rest_id).first()
    db.session.delete(favorite_restaurant)
    db.session.commit()
    return redirect(f'/restaurant/{rest_id}')