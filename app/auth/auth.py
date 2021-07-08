from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.auth import bp
from app.func import bp as function
from app import app, db
from flask_login import current_user , login_user, login_required, logout_user

@bp.route('/')
def home():
    return render_template('auth/home.html')

@bp.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        #Query through out the database to find the user with a specific username and return first result
        user = User.query.filter_by(username = username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('You are logged in', category = 'success')
                login_user(user, remember = True) # logs in user which allows acess to users data
                return redirect(url_for('auth.home'))
            else:
                flash('Wrong password')
        else:
            flash ('User does not exist')
    return render_template('auth/login.html')

@bp.route('/signup', methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        retype = request.form.get('Retype')
        
        if email.find('@') == 1 and email.find('.') == 1:
            flash('Email is Invalid',category = 'error')
        elif len(password)<8:
            flash('Password is too short',category = 'error')
        elif password != retype:
            flash('Password is not the same',category = 'error')
        else:
            #creates user
            new_user = User(email=email, username=username, 
                password=generate_password_hash(password))
            #adds user to database
            db.session.add(new_user)
            #updates database
            db.session.commit()
            #redirects to homepage after sign up
            return redirect(url_for('auth.home'))
            
    return render_template('auth/signup.html', user = current_user)

@login_required
@bp.route('/logout',methods = ['POST', 'GET'])
def logout():
    logout_user()
    redirect(url_for('auth.login'))

    

