import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'a-very-secret-scooter'
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
