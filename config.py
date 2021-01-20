import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'sqlite:///' + os.path.join(basedir, 'main.db')

  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
  SQLALCHEMY_TRACK_MODIFICATIONS = False

