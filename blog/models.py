from datetime import datetime

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from flask_login import UserMixin


db = SQLAlchemy()
login_manager = LoginManager()


class Post(db.Model):
	"""docstring for Posts"""

	__tablename__ = 'post'

	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable = False, info = {"limit": 100})
	text = db.Column(db.Text, nullable = False)
	path_img = db.Column(db.String, nullable = True)
	pub_date = db.Column(db.DateTime, nullable = False, default = datetime.now())
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = False)
	category = db.relationship('Category', backref = db.backref('posts', lazy = True))


	def get_PubDate(self):
		return self.pub_date.strftime("%d.%m.%Y/%H:%M")


	def __repr__(self):
		return f"{self.title} - id: {self.id}"


class Category(db.Model):
	"""docstring for Category"""

	__tablename__ = 'category'

	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable = False, info = {"limit": 100})
	slug = db.Column(db.String(100), nullable = False, info = {"limit": 100})


	def __repr__(self):
		return self.slug


class User(UserMixin, db.Model):
	"""docstring for Category"""

	__tablename__ = 'user'

	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(128), nullable = False, info = {"limit": 128})
	email = db.Column(db.String(255), unique = True, info = {"limit": 255})
	password = db.Column(db.String(255), nullable = False, info = {"limit": 255})
	email_newsletter = db.Column(db.Boolean, default = False, nullable = False)


	def set_password(self, password):
		self.password = generate_password_hash(password)


	def check_password(self, password):
		return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
