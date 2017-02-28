#coding=utf-8
from flask import Flask, render_template
from flask import request
from flask import make_response
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess what dog'
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

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

@app.route('/testpost', methods=['GET', 'POST'])
def testpost():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('TestPost.html', form=form, name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

class NameForm(FlaskForm):
    name = StringField(u'你的名字是什么?', validators=[Required()])
    submit = SubmitField('Submit')

if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()
