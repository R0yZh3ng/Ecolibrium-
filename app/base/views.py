from flask import render_template, redirect, url_for, Blueprint, request, current_app
from flask_login import current_user, login_required
from app.__init__ import bcrypt

from flask import jsonify
from sqlalchemy import desc
#from app.user.models import User
from app import db

from datetime import date, timedelta

from . import base_blueprint

@base_blueprint.route('/')
def main():
    user = current_user
    return render_template("base/main.html", user = user)

@base_blueprint.route('/about_us')
def about_us():
    user = current_user
    return render_template("base/about_us.html", user=user)