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
from views import management

from mailing import send_messages


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
app.register_blueprint(management)

login_manager.init_app(app)
login_manager.login_view = 'management.login'


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



def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_usets_emails():
	users = User.query.filter_by(email_newsletter = True).all()
	emails_for_newsletter = [user.email for user in users]

	return emails_for_newsletter

@app.route("/create", methods = ["POST", "GET"])
@login_required
def create():
	data = {
		"categories": Category.query.all(),
		"limit_title": Post.title.info["limit"],
	}

	if request.method == "POST":
		title = request.form.get("title")
		text = request.form.get("text")
		image = request.files.get("image")

		category = request.form.get("category")
		category = Category.query.filter_by(slug = category).first()

		if not (title and text and category):
			flash("Not all fields are filled")
			return render_template("create.html", data = data)

		post = Post(title = title, text = text, category = category)

		if image and allowed_file(image.filename):
			filename = secure_filename(image.filename)
			image.save(os.path.join(UPLOADS_PATH, app.config['UPLOAD_FOLDER'], filename))

			post.path_img = f"./media/{filename}"

		try:
			db.session.add(post)
			db.session.commit()

			emails = get_usets_emails()

			if emails:
				send_messages(emails = emails)

			return redirect(url_for("index"))
		except:
			return "Error"

	return render_template("create.html", data = data)


if __name__ == '__main__':
	app.run(debug = True)
