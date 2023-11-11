from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = 'user_login'

import os

bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder='../template')
    app.config['SECRET_KEY'] = os.urandom(16).hex()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)

    from .base.views import base_blueprint
    app.register_blueprint(base_blueprint, url_prefix='/')
    from .user.views import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix = '/')

    @login_manager.user_loader
    def load_user(user_id):
        from .user.models import User
        return User.query.get(int(user.id))
    return app