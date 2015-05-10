from app import db
import datetime

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column('nickname', db.String(64), index=True, unique=True)
    email = db.Column('email', db.String(120), index=True, unique=True)
    password = db.Column('password', db.String(50))
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, nickname, password, email):
        self.nickname = nickname
        self.password = password
        self.email = email

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def is_authenticated(self):
        return True

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, body, author):
        self.body = body
        self.timestamp = datetime.datetime.now()
        self.author = author

    def __repr__(self):
        return '<Post %r>' % (self.body)