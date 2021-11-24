from models import db
from app import create_app
from models import Post, Category

app = create_app()
app.app_context().push()
db.create_all()

category_1 = Category(title = "Python", slug = "python")
category_2 = Category(title = "JavaScript", slug = "javascript")
post_1 = Post(title = "Title post 1", text = "Text post 1", category = category_1, path_img = "./media/post-img-1.jpg")
post_2 = Post(title = "Title post 2", text = "Text post 2", category = category_2, path_img = "./media/post-img-2.jpg")
db.session.add(category_1)
db.session.add(category_2)
db.session.add(post_1)
db.session.add(post_2)
db.session.commit()