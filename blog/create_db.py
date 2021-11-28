from models import db
from models import Post
from models import Category

from app import create_app


app = create_app()
app.app_context().push()
db.create_all()

category_1 = Category(title = "Python", slug = "python")
category_2 = Category(title = "JavaScript", slug = "javascript")
post_1 = Post(title = "Title post 1", text = "Text post 1", category = category_1, path_img = "./media/post-img-1.jpg")
post_2 = Post(title = "Title post 2", text = "Text post 2", category = category_2, path_img = "./media/post-img-2.jpg")
post_3 = Post(title = "Title post 3", text = "Text post 3", category = category_1, path_img = "./media/post-img-3.jpg")
post_4 = Post(title = "Title post 4", text = "Text post 4", category = category_1, path_img = "./media/post-img-4.jpg")

db.session.add(category_1)
db.session.add(category_2)

db.session.add(post_1)
db.session.add(post_2)
db.session.add(post_3)
db.session.add(post_4)

db.session.commit()
