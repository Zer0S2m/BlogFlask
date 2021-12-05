import os


UPLOAD_FOLDER = "static/media"
UPLOADS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)))

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

FOLDER_STATIC = "static"
NAME_DB = "blog.db"
PER_PAGE = 3

SECRET_KEY = "qwerty"

# Для рассылки писем
EMAIL = ""
EMAIL_PASSWORD = ""
