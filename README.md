# Blog Flask

1. **pip install -r requirements.txt**
2. **go to directory "./blog"**
3. **Start '_Python_':**

```python
>>> from app import db
>>> db.create_all()
```

4. **Create multiple articles:**

```python
>>> from app import Post
>>> post_1 = Post(title = "Title post-1", text = "Text post-1")
>>> post_2 = Post(title = "Title post-2", text = "Text post-2")
>>> db.session.add(post_1)
>>> db.session.add(post_2)
>>> db.session.commit()
```
