import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    #DEBUG = False
    TESTING = True

    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join('.'+basedir, 'user.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'heythisisthesecretkey'
    

