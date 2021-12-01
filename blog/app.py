import os
from werkzeug.utils import secure_filename

from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from flask import flash

from flask_login import login_required
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user

from models import db
from models import Post
from models import Category
from models import User
from models import login_manager

from config import UPLOAD_FOLDER
from config import UPLOADS_PATH
from config import ALLOWED_EXTENSIONS
from config import FOLDER_STATIC
from config import NAME_DB
from config import PER_PAGE
from config import SECRET_KEY

from views import category


def create_app():
	app = Flask(__name__, static_folder = FOLDER_STATIC)
	app.secret_key = SECRET_KEY

	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{NAME_DB}'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

	db.init_app(app)

	return app


app = create_app()
app.register_blueprint(category)

login_manager.init_app(app)
login_manager.login_view = 'login'


@app.errorhandler(404)
def notFoundError(error):
	return render_template('404.html'), 404


@app.route("/", methods = ["GET"], defaults = {"page": 1})
@app.route("/<int:page>", methods = ["GET"])
def index(page):
	pagination = Post.query.order_by(Post.pub_date.desc()).paginate(page, PER_PAGE, error_out = False)

	data = {
		"pagination": pagination
	}

	return render_template("index.html", data = data)


@app.route("/about")
def about():
	return render_template("about.html")


@app.route("/post-<int:id>")
def post_detail(id):
	post = Post.query.filter_by(id = id).first()

	data = {
		"post": post
	}

	return render_template("postDetail.html", data = data)



def allowedFile(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/create", methods = ["POST", "GET"])
@login_required
def create():
	if request.method == "POST":
		title = request.form["title"]
		text = request.form["text"]
		image = request.files["image"]

		category = request.form["category"]
		category = Category.query.filter_by(slug = category).first()

		post = Post(title = title, text = text, category = category)

		if image and allowedFile(image.filename):
			filename = secure_filename(image.filename)
			image.save(os.path.join(UPLOADS_PATH, app.config['UPLOAD_FOLDER'], filename))

			post.path_img = f"./media/{filename}"

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


@app.route('/login', methods = ['POST', 'GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("index"))

	if request.method == 'POST':
		email = request.form['email']
		user = User.query.filter_by(email = email).first()

		if user is not None and user.check_password(request.form['password']):
			login_user(user)
			return redirect(url_for("index"))

	return render_template('control/login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("index"))

	if request.method == 'POST':
		email = request.form.get('email')
		username = request.form.get('username')
		password = request.form.get('password')

		if not (email and username and password):
			flash('You did not provide data')
			return redirect(url_for('register'))

		user = User(username = username, email = email)

		user.set_password(password)
		db.session.add(user)
		db.session.commit()

		return redirect(url_for("login"))

	return render_template('control/register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == '__main__':
	app.run(debug = True)
