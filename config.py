import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS= os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    PORTFOLIO_MAIL_SUBJECT_PREFIX = '[Portfolio Email]'
    PORTFOLIO_MAIL_SENDER = os.environ.get('PORTFOLIO_MAIL_SENDER')
    PORTFOLIO_ADMIN = os.environ.get('PORTFOLIO_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BLOG_POSTS_PER_PAGE = os.environ.get('BLOG_POSTS_PER_PAGE')
    PROJECTS_PER_PAGE = os.environ.get('PROJECTS_PER_PAGE')
    BASEDIR = basedir
    VIDEO_PER_PAGE=os.environ.get('VIDEO_PER_PAGE')
    PORTFOLIO_BLOGGER=os.environ.get('PORTFOLIO_BLOGGER')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}