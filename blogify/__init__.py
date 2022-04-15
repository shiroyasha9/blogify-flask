# blogify/__init__.py
from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

# Login Configs
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users_posts.login'

# Error handling

@app.errorhandler(404)
def error_404(error):
  return render_template('error_pages/404.html'), 404

@app.errorhandler(403)
def error_403(error):
  return render_template('error_pages/403.html'), 403

from blogify.core.views import core
from blogify.users_posts.views import users_posts

app.register_blueprint(core)
app.register_blueprint(users_posts)