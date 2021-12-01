from flask import Blueprint
from flask import render_template

from models import Post
from models import Category


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
