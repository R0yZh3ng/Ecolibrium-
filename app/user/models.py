from datetime import datetime, date
from app import db
from app import bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique= True)
    password_hash = db.Column(db.String(128))
    registered_on = db.Column(db.DateTime, default = datetime.utcnow )
    
    def __repr__(self):
        return f'<User {self.display_name}>'
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)