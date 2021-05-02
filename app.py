
from flask import Flask, render_template, redirect, flash, session
from models import db, connect_db, User, Rating, Favorite, Comment, LikeDislike
from forms import RegisterForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///local'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'helloworld'

connect_db(app)
db.create_all()


@app.route('/')
def homepage():
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
                                      location,
                                      email,
                                      password)
        db.session.add(register_user)
        db.session.commit()
        session['user_id'] = register_user.email
        return redirect('/')
    return render_template('register.j2', form=form)