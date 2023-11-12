from flask import render_template, redirect, url_for, Blueprint, request, current_app, flash

from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash

from app.user.forms import RegistrationForm
from app.user.forms import LoginForm
from app.user.models import User
from app.forum.models import Forum
from app import db
from app.__init__ import bcrypt

from . import user_blueprint

@user_blueprint.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember = form.remember.data)
            return redirect(url_for('forums.home'))
        else:
            flash('Login Unsuccessful, please check the username and password', 'danger')

    return render_template('user/login.html', title = 'login', form = form)

@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base.home'))

@user_blueprint.route('/register', methods=['GET, POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username = form.username.data,
            password_hash = hashed_password
        )

        db.session.add(user)
        db.session.commit()
        flash('Your account has been created, please login using the set credentials')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', title = 'Register', form= form)

@user_blueprint.route('/view_profile', methods= ['GET, POST'])
def view_profile(user_id):
    user_all_forums = Forum.query.options(db.joinedload(Forum.creator)).filter_by(creator_id=user_id, private = False).all()
    username = User.query.get_or_404(user_id)

    return render_template('user/view_profile.html', username = username, user_all_forums = user_all_forums)
