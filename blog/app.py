from flask import Flask
from flask import render_template
from flask import url_for

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Post(db.Model):
	"""docstring for Posts"""

	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable = False)
	text = db.Column(db.Text, nullable = False)


	def __repr__(self):
		return self.title


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


if __name__ == '__main__':
	app.run(debug = True)
