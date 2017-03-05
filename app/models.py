#coding=utf8
from . import db

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    users = db.relationship('User', backref='role') # backref的属性值将添加到对应关系表中

    def __repr__(self):
        return  '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique=True, index = True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    sex = db.Column(db.Integer,  default=1)

    def __repr__(self):
        return  '<User %r>' % self.username