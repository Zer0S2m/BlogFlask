from datetime import datetime

from flask import Flask
from flask import render_template
from flask import url_for

from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__, static_folder = "static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Post(db.Model):
	"""docstring for Posts"""

	id = db.Column(db.Integer(), primary_key = True)
	title = db.Column(db.String(100), nullable = False)
	text = db.Column(db.Text(), nullable = False)
	pathImg = db.Column(db.String(), nullable = True)
	pubDate = db.Column(db.DateTime(), nullable = False, default = datetime.now().date())


	def __repr__(self):
		return f"{self.title} - id: {self.id}"


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


@app.route("/post-<int:id>")
def postDetail(id):
	post = Post.query.filter_by(id = id).first()

	data = {
		"post": post
	}

	return render_template("postDetail.html", data = data)


if __name__ == '__main__':
	app.run(debug = True)
