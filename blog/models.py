from datetime import datetime
from datetime import date

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Post(db.Model):
	"""docstring for Posts"""

	__tablename__ = 'post'

	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable = False)
	text = db.Column(db.Text, nullable = False)
	path_img = db.Column(db.String, nullable = True)
	pub_date = db.Column(db.DateTime, nullable = False, default = date.today())
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = False)
	category = db.relationship('Category', backref = db.backref('posts', lazy = True))


	def __repr__(self):
		return f"{self.title} - id: {self.id}"


class Category(db.Model):
	"""docstring for Category"""

	__tablename__ = 'category'

	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable = False)
	slug = db.Column(db.String(50), nullable = False)


	def __repr__(self):
		return self.slug
