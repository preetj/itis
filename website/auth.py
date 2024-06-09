from flask import Blueprint, render_template, request, flash,redirect,url_for
from .models import User
from . import db
import re
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
import os 
from .config import SECRET_KEY







auth = Blueprint('auth', __name__)

#In-Memory token storage
reset_tokens = {}


def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt='reset-password')



def confirm_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(token, salt='reset-password', max_age=expiration)
    except:
        return None
    return email

from flask import render_template, redirect, url_for
from flask_login import current_user

from flask import render_template, redirect, url_for, request

@auth.route('/reset-password', methods=['GET', 'POST'])
def request_password_reset():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = generate_reset_token(user.email)
            reset_tokens[token] = user.email
            flash(f'Token generated: {token}', 'info') # Displaying the token
            return redirect(url_for('auth.reset_password', token=token))
        flash('The email is not registered', category='error')
    
    # Render the password reset request form
    return render_template('request_reset.html')




@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = confirm_reset_token(token)
    if not email:
        flash('The reset link is invalid or has expired', 'error')
        return redirect(url_for('auth.request_password_reset'))
    if request.method == 'POST':
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = generate_password_hash(password, method='sha256')
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('auth.login'))
    return render_template('reset_password.html')




def strong_password(password):
    if len(password) <7:
        return False
    if not re.search('[a-z]', password):
        return False
    if not re.search('[A-Z]', password):
        return False
    if not re.search('[0-9]', password):
        return False
    if not re.search('[@#$%^&+=]', password):
        return False
    return True

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!', category='success')
                login_user(user, remember=True)
                if user.role == 'admin':  # Redirect to admin home if user is admin
                    return redirect(url_for('views.admin_home'))
                else:  # Redirect to regular home if user is not admin
                    return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, try again', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if email == 'admin@gmail.com' and password1 == 'Admin@123':
            role = 'admin'
        else:
            role = 'user'

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'), role=role)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)



