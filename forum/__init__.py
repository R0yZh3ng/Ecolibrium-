from flask import Blueprint

forum_blueprint = Blueprint('forum', __name__)

from app import db

with app.app_context():
    db.create_all()