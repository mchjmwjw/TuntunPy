from flask import Flask, render_template, Blueprint
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment();
db = SQLAlchemy();
main = Blueprint('main', __name__)

# 工厂函数
def create_app(cobfig_name):
    app = Flask(__name__)
    app.config.from_object(config[cobfig_name])
    config[cobfig_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # 注册蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

from . import views, errors