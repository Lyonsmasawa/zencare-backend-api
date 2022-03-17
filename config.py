import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:passdb@localhost/zen'
    JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace('postgres://', 'postgresql://')
    pass

class TestConfig(Config):
    pass

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:passdb@localhost/zen'
    DEBUG = True

config_options = {
    'development': DevConfig,
    'production': ProdConfig,
    'test': TestConfig
}