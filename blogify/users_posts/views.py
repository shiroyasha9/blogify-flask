from flask import abort, render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blogify import db
from blogify.models import User, BlogPost
from blogify.users_posts.forms import RegistrationForm, LoginForm, BlogPostForm

users_posts = Blueprint('users_posts', __name__)

# user views
@users_posts.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()

  if form.validate_on_submit():
    user = User(email = form.email.data, password=form.password.data, username = form.username.data)
    db.session.add(user)
    db.session.commit()
    flash('Thanks for registration!')
    return redirect(url_for('users_posts.login'))
  
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

@users_posts.route('/account', methods=['GET', 'POST'])
@login_required
def account():
  username = current_user.username
  email = current_user.email
  display_picture = f'https://ui-avatars.com/api/?name={username[0]}'
  return render_template('account.html', username=username, email=email, display_picture = display_picture)

@users_posts.route('/<username>')
def user_posts(username):
  page = request.args.get('page', 1, type=int)
  user = User.query.filter_by(username=username).first_or_404()
  blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
  display_picture = f'https://ui-avatars.com/api/?name={username[0]}'
  return render_template('user_blog_posts.html', blog_posts = blog_posts, user = user, display_picture = display_picture)
  
# blog views
@users_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
  form  = BlogPostForm()
  
  if form.validate_on_submit():
    blog_post = BlogPost(title = form.title.data, text = form.text.data, user_id = current_user.id)
    db.session.add(blog_post)
    db.session.commit()
    flash('Blog Post Created')
    return redirect(url_for('core.index'))
  
  return render_template('create_post.html', form = form)
  
@users_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
  blog_post = BlogPost.query.get_or_404(blog_post_id)
  return render_template('blog_post.html', post = blog_post)

@users_posts.route('/<int:blog_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(blog_post_id):
  blog_post = BlogPost.query.get_or_404(blog_post_id)
  if blog_post.author != current_user:
    abort(403)
  
  db.session.delete(blog_post)
  db.session.commit()
  flash('Blog Post Deleted')
  return redirect(url_for('core.index'))
  
