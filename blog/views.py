from flask import Blueprint
from flask import render_template

from models import Post
from models import Category


categories_blueprint = Blueprint('categories', __name__, template_folder = 'templates')

@categories_blueprint.route("/categories")
def categories():
	infoPosts = {}

	categories = Category.query.all()

	for category in range(0, len(categories)):
		postsCount = len(Post.query.filter_by(category = categories[category]).all())
		infoPosts[categories[category]] = postsCount

	data = {
		"categories": categories,
		"infoPosts": infoPosts,
	}

	return render_template("categories.html", data = data)


categoryDetail_blueprint = Blueprint('category', __name__, template_folder = 'templates')

@categoryDetail_blueprint.route("/category/<slug>")
def categoryDetail(slug):
	category = Category.query.filter_by(slug = slug).first()
	posts = Post.query.filter_by(category = category).all()

	data = {
		"slug": slug,
		"title": category.title,
		"posts": posts
	}

	return render_template("categoryDetail.html", data = data)
