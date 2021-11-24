from flask import Flask
from flask import render_template
from flask import url_for

from models import db
from models import Post


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
	print(posts)

	data = {
		"posts": posts
	}

	return render_template("index.html", data = data)


@app.route("/about")
def about():
	return render_template("about.html")


@app.route("/post-<int:id>")
def postDetail(id):
	post = Post.query.filter_by(id = id).first()

	data = {
		"post": post
	}

	return render_template("postDetail.html", data = data)


if __name__ == '__main__':
	app.run(debug = True)
