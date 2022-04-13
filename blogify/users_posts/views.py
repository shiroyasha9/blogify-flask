from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blogify import db
from blogify.models import User, BlogPost
from blogify.users_posts.forms import RegistrationForm, LoginForm

users_posts = Blueprint('users_posts', __name__)

@users_posts.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()

  if form.validate_on_submit():
    user = User(email = form.email.data, password=form.password.data, username = form.username.data)
    db.session.add(user)
    db.session.commit()
    flash('Thanks for registration!')
    return redirect(url_for(users_posts.login))
  
  return render_template('register.html', form=form)


@users_posts.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user.check_password(form.password.data) and user is not None:
      login_user(user)
      flash('Log in successfully!')

      next = request.args.get('next')
      if next == None or not next[0] == '/':
        next = url_for('core.index')
      
      return redirect(next)
  
  return render_template('login.html', form=form)

@users_posts.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('core.index'))