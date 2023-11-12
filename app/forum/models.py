from datetime import datetime
from app import db
from app.user.models import User

class Forum(db.Model):
    __tablename__ = 'forum'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(256), nullable = False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)

    comments = db.relationship('Comment', backref='forum', lazy=True)
    creator = db.relationship('User', backref='forums')


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'), nullable=False)

    creator = db.relationship('User', backref='comment')

    def __repr__(self):
        return f'<comment {self.title}>'


def init_db():
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    init_db()