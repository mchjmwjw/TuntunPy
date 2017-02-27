#coding=utf-8
from flask import Flask, render_template
from flask import request
from flask import make_response
from flask_script import Manager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')
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

if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()
