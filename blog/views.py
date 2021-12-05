from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import flash

from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required

from models import Post
from models import Category
from models import User
from models import db


category = Blueprint('category', __name__, template_folder = 'templates')


@category.route("/categories")
def category_list():
	info_posts = {}

	categories = Category.query.all()

	for category in range(0, len(categories)):
		postsCount = len(Post.query.filter_by(category = categories[category]).all())
		info_posts[categories[category]] = postsCount

	data = {
		"categories": categories,
		"info_posts": info_posts,
	}

	return render_template("categories.html", data = data)


@category.route("/categories/<slug>")
def category_detail(slug):
	category = Category.query.filter_by(slug = slug).first()
	posts = Post.query.filter_by(category = category).all()

	data = {
		"slug": slug,
		"title": category.title,
		"posts": posts
	}

	return render_template("categoryDetail.html", data = data)


management = Blueprint('management', __name__, template_folder = 'templates/management')


@management.route('/login', methods = ['POST', 'GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("index"))

	if request.method == 'POST':
		email = request.form.get('email')
		user = User.query.filter_by(email = email).first()

		if user is not None and user.check_password(request.form.get('password')):
			login_user(user)
			return redirect(url_for("index"))

	return render_template('login.html')


@management.route('/register', methods=['POST', 'GET'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("index"))

	if request.method == 'POST':
		email = request.form.get('email')
		username = request.form.get('username')
		password = request.form.get('password')
		repeat_password = request.form.get('repeat_password')
		email_newsletter = request.form.get('email_newsletter')

		if email_newsletter == "on":
			email_newsletter = True
		else:
			email_newsletter = False

		if User.query.filter_by(email = email).first():
			flash('User with this email already exists')
			return redirect(url_for('management.register'))

		if not (email and username and password):
			flash('You did not provide data')
			return redirect(url_for('management.register'))

		if password != repeat_password:
			flash('Password mismatch')
			return redirect(url_for('management.register'))

		user = User(username = username, email = email, email_newsletter = email_newsletter)

		user.set_password(password)
		db.session.add(user)
		db.session.commit()

		return redirect(url_for("management.login"))

	return render_template('register.html')


@management.route("/cabinet", methods = ["GET", "POST"])
@login_required
def cabinet():
	if request.method == "POST":
		email = request.form.get('email')
		username = request.form.get('username')
		email_newsletter = request.form.get('email_newsletter')

		if email_newsletter == "on":
			email_newsletter = True
		else:
			email_newsletter = False

		user = User.query.filter_by(email = current_user.email).first()

		user.username = username
		user.email = email
		user.email_newsletter = email_newsletter

		db.session.commit()

		return redirect(url_for("management.cabinet"))

	return render_template("cabinet.html")


@management.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))
