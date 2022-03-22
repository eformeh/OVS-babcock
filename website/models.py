from . import db
from flask_login import UserMixin
# from datetime import datetime


# for timezone
# from sqlalchemy.sql import func

# tables in database

# class users(db.Model, UserMixin):
#    id = db.Column(db.Integer, primary_key=True)
#    email = db.Column(db.String(150), db.ForeignKey('students.email'))
#    password = db.Column(db.String(150), db.ForeignKey('students.password'))

class students(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    password = db.Column(db.String(150))
    choice = db.Column(db.String(150))
    choice2 = db.Column(db.String(150))
    has_voted = db.Column(db.Integer, default = 0)


class admin (db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    adminUsername = db.Column(db.String(150), unique=True)
    adminPassword = db.Column(db.String(150))


class president (db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    manifesto = db.Column(db.String(1000))
    post = db.Column(db.String(150))
    vote_count = db.Column(db.Integer, default=0)

#    candidate_pic = db.Column(db.String, unique=True, nullable=True)
#    candidate_pic_name = db.Column(db.String, unique=True, nullable=True)
#    mimetype = db.Column(db.Text, nullable=True)


class vice(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    vote_count = db.Column(db.Integer, default=0)
    manifesto = db.Column(db.String(1000))
    post = db.Column(db.String(150))


# store the voter id when voted
class poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer)
