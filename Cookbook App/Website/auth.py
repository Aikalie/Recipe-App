from xmlrpc.client import boolean
from flask import Blueprint, render_template, request, flash, redirect, url_for
from . models import User
from werkzeug.security import generate_password_hash, check_password_hash #scrambles the password
from . import db
from flask_login import login_user, login_required, logout_user, current_user   #flask plugins that let you easily track logged user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() #search database for users with the entered email and give the first result
        if user:
            if check_password_hash(user.password, password):    #check hashed password from database against password entered here
                flash('Logged in successfully', category='success')
                login_user(user, remember=True) #store logged in user in their browser session
                return redirect(url_for('views.home'))  #redirect to home listed in views.py
            else:
                flash('Incorrect email/password', category='error')
        else:
            flash('Incorrect email/password', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))  #bring user back to login screen

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first() #search database for users with the entered email and give the first result

        if user:    #determine if account already created using this email
            flash('Email already exists', category='error')
        elif len(email) < 4: #if email is shorter than 4 characters
            flash('Email must be greater than 4 characters', category='error')
        elif password1 != password2:    #if passwords don't match
            flash('Passwords do not match', category='error')
        elif len(password1) < 7:    #if password shorter than 7 characters
            flash('Pass must be at least 7 characters', category='error')
        else:   #add user to database
            new_user = User(email=email, firstName=first_name, password=generate_password_hash(password1, method='sha256')) #hashes password, sha256 is a hashing algorithm
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True) #store logged in user in their browser session
            flash('Account created!', category='success')
            return redirect(url_for('views.home')) #takes the user back to the homepage after account created
    
    return render_template("sign_up.html", user=current_user)