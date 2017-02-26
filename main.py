#coding=utf-8
from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '<h1>Hello World!</h1><br>' + u'<p>Your 浏览器 is %s' % user_agent

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name

if __name__ == '__main__':
    app.run(debug=True)
