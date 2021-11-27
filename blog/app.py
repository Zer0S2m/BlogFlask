from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import request

from models import db
from models import Post
from models import Category


def create_app():
	app = Flask(__name__, static_folder = "static")
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	db.init_app(app)

	return app


app = create_app()


@app.route("/index")
@app.route("/")
def index():
	posts = Post.query.all()

	data = {
		"posts": posts
	}

	return render_template("index.html", data = data)


@app.route("/about")
def about():
	return render_template("about.html")


@app.route("/categories")
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


@app.route("/post-<int:id>")
def postDetail(id):
	post = Post.query.filter_by(id = id).first()

	data = {
		"post": post
	}

	return render_template("postDetail.html", data = data)


@app.route("/category/<slug>")
def categoryDetail(slug):
	category = Category.query.filter_by(slug = slug).first()
	posts = Post.query.filter_by(category = category).all()

	data = {
		"slug": slug,
		"title": category.title,
		"posts": posts
	}

	return render_template("categoryDetail.html", data = data)


@app.route("/create", methods = ["POST", "GET"])
def create():
	if request.method == "POST":
		title = request.form["title"]
		text = request.form["text"]

		category = request.form["category"]
		category = Category.query.filter_by(slug = category).first()

		post = Post(title = title, text = text, category = category)

		try:
			db.session.add(post)
			db.session.commit()

			return redirect("/")
		except:
			return "Error"

	else:
		categories = Category.query.all()

		data = {
			"categories": categories,
		}

		return render_template("create.html", data = data)


if __name__ == '__main__':
	app.run(debug = True)
