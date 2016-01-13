__author__ = 'FRAMGIA\nguyen.huy.quyet'

from os.path import abspath, dirname, join

_cwd = dirname(abspath(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'flask-session-insecure-secret-key'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_cwd, 'data.db')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@hoada921@localhost:5432/flask'
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
