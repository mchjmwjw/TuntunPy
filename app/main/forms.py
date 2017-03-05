#coding=utf8
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import Required

class NameForm(FlaskForm):
    name = StringField(u'你的名字是什么?', validators=[Required()])
    submit = SubmitField('Submit')