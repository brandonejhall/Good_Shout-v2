from sqlalchemy.orm import backref, relation, relationship
from app import db, login #importing db from the current package
from flask_login import UserMixin # flask_login is a module which assists with the loging in of users
from sqlalchemy.sql import func

comments = db.Table('commenters', 
    db.Column('shout_id',db.Integer, db.ForeignKey('shouts.id')),
    db.Column('fixture_id',db.Integer, db.ForeignKey('fixtures.id'))
)

class Shouts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(360))
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
     

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(40), unique = True)
    password = db.Column(db.String(50))
    email = db.Column(db.String(100))
    shouts = db.relationship('Shouts')

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Fixtures(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    home = db.Column(db.String, unique = True)
    home_score = db.Column(db.Integer)
    away = db.Column(db.String, unique = True)
    away_score = db.Column(db.Integer)
    comments = db.relationship('Shouts',secondary = comments, backref = db.backref('commentors', lazy = 'dynamic'))


#person  =  User( username = 'ThisIsBrandon', password = 'ThisIsAPassword', email = 'ThisIsAEmail@email.com')

