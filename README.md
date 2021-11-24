# Blog Flask

1. **pip install -r requirements.txt**
2. **go to directory "./blog"**
3. **Start '_Python_'**
4. **Create a database:**

```python
>>> from app import db
>>> db.create_all()
```

5. **Create multiple articles:**

```python
>>> from app import Post
>>> post_1 = Post(title = "Title post 1", text = "Text post 1", pathImg = "./media/post-img-1.jpg")
>>> post_2 = Post(title = "Title post 2", text = "Text post 2", pathImg = "./media/post-img-2.jpg")
>>> db.session.add(post_1)
>>> db.session.add(post_2)
>>> db.session.commit()
```
