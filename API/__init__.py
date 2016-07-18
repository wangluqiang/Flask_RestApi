# coding=utf-8
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from config import config

db = SQLAlchemy()
auth = HTTPBasicAuth()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))
    db.init_app(app)
    from .task.views import task_blueprnt
    app.register_blueprint(task_blueprnt, url_prefix='/todo/api/v1.0')
    from .users.views import users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/todo/api/v1.0')
    return app
