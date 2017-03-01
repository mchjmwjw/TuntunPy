#coding=utf-8

from flask import Flask, render_template, session, redirect, url_for, flash
from flask import request
from flask import make_response
from flask_script import Manager
from flask_script import Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
import platform
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail
from flask_mail import Message
from threading import Thread

basedir = path.abspath(path.dirname(__file__))
opesys = platform.system()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess what dog'
if opesys is 'Windows':
    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + path.join(basedir, 'dbs/tuntunpy.db')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:////' + path.join(basedir, 'dbs/tuntunpy.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # 每次请求结束后自动提交数据库中的变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['TUNTUNPY_MAIL_SUBJECT_PREFIX'] = '[TuntunPy]'  # 邮件主题的前缀
app.config['TUNTUNPY_MAIL_SENDER'] = 'Hoster Wang <' + str(app.config['MAIL_USERNAME']) + '>'  # 发件人地址
app.config['TUNTUNPY_ADMIN'] = os.environ.get('TUNTUNPY_ADMIN')  # 电子邮件收件人

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())
    # user_agent = request.headers.get('User-Agent')
    # return '<h1>Hello World!</h1><br>' + u'<p>Your 浏览器 is %s' % user_agent

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
    # return '<h1>Hello, %s!</h1>' % name

@app.route('/cook')
def cook():
    response = make_response(u'<h1>这个文件携带了一个cookie</h1>')
    response.set_cookie('answer', '42')
    return response

@app.route('/testpost2', methods=['GET', 'POST'])
def testpost():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['TUNTUNPY_ADMIN']:
                send_email(app.config['TUNTUNPY_ADMIN'], user.username,
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash(u'你输入的名称已经改变！')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('testpost'))
    return render_template('TestPost.html', form=form, name=session.get('name'), known=session.get('known', False))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 4

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

class NameForm(FlaskForm):
    name = StringField(u'你的名字是什么?', validators=[Required()])
    submit = SubmitField('Submit')

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

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['TUNTUNPY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['TUNTUNPY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
    # mail.send(msg)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()
