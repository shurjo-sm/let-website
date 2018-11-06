from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, NewsPost, SecurePost
from app.forms import LoginForm, NewsPostForm, SecurePostForm
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
	post_titles = [{'title': post.title, 'timestamp': '{}/{}/{}'.format(post.timestamp.day, post.timestamp.month, post.timestamp.year), 'id': post.id } for post in NewsPost.query.all()]
	post_titles.reverse()
	post_titles = post_titles[0:6]
	return render_template('index.html', post_titles=post_titles, title='Little Einsteins\' Tutorial')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flask('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/news')
def news():
	posts = [{'title': post.title, 'body': post.body, 'timestamp': '{}/{}/{}'.format(post.timestamp.day, post.timestamp.month, post.timestamp.year), 'id': post.id } for post in NewsPost.query.all()]
	posts.reverse()
	return render_template('news.html', posts=posts, title='News and Events', heading='News and Events')

@app.route('/parentsarea')
@login_required
def parentsarea():
	posts = [{'title': post.title, 'body': post.body, 'timestamp': '{}/{}/{}'.format(post.timestamp.day, post.timestamp.month, post.timestamp.year), 'id': post.id } for post in SecurePost.query.all()]
	posts.reverse()
	return render_template('parentsarea.html', posts=posts, title='Parent\'s Area', heading='Parent\'s Area')

@app.route('/admission')
def admission():
	return render_template('admission.html', title='Admission')

@app.route('/adminpanel', methods=['GET', 'POST'])
@login_required
def adminpanel():
	if not current_user.username == 'admin':
		flash('You must be admin to access this page')
		return redirect(url_for('login'))
	return render_template('admin.html', title='Admin Panel')

@app.route('/adminpanel/new_newspost', methods=['GET', 'POST'])
@login_required
def new_newspost():
	if not current_user.username =='admin':
		flash('You must be damin to access this page')
		return redirect(url_for('login'))
	form = NewsPostForm()
	if form.validate_on_submit():
		newspost = NewsPost(title=form.title.data, body=form.body.data)
		db.session.add(newspost)
		db.session.commit()
		flash('Your post is now live!')
		return redirect(url_for('index'))
	return render_template('new_post.html', form=form, title='New News Post')

@app.route('/adminpanel/new_securepost', methods=['GET', 'POST'])
@login_required
def new_securepost():
	if not current_user.username =='admin':
		flash('You must be damin to access this page')
		return redirect(url_for('login'))
	form = SecurePostForm()
	if form.validate_on_submit():
		securepost = SecurePost(title=form.title.data, body=form.body.data)
		db.session.add(securepost)
		db.session.commit()
		flash('Your post is now live!')
		return redirect(url_for('index'))
	return render_template('new_post.html', form=form, title='New Secure Post')

@app.route('/news/<id>')
def newspost(id):
	newspost = NewsPost.query.filter_by(id=id).first_or_404()
	return render_template('post.html', title=newspost.title, post=newspost, timestamp='{}/{}/{}'.format(newspost.timestamp.day, newspost.timestamp.month, newspost.timestamp.year))

@app.route('/parentsarea/<id>')
@login_required
def securepost(id):
	securepost = SecurePost.query.filter_by(id=id).first_or_404()
	return render_template('post.html', title=securepost.title, post=securepost, timestamp='{}/{}/{}'.format(securepost.timestamp.day, securepost.timestamp.month, securepost.timestamp.year))