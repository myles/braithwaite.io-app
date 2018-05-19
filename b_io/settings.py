from os import environ
from pathlib import Path


class Config(object):
    """Base configuration."""

    SECRET_KEY = environ.get('B_IO_SECRET', 'secret-key')

    PROJECT_ROOT = Path(__file__).parents[1]
    APP_DIR = Path(__file__).parents[0]

    STATIC_FOLDER = APP_DIR.joinpath('static')
    TEMPLATES_FOLDER = STATIC_FOLDER = APP_DIR.joinpath('templates')
    CONTENT_ROOT = environ.get(
        'B_IO_CONTENT_PATH', PROJECT_ROOT.joinpath('content'))

    GITHUB_REPO = environ.get(
        'B_IO_GITHUB_REPO',
        'https://github.com/myles/braithwaite.io-notebook')

    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    FREEZER_DESTINATION = environ.get(
        'B_IO_BUILD_PATH', PROJECT_ROOT.joinpath('build'))
    FREEZER_IGNORE_MIMETYPE_WARNINGS = True

    WEBMENTION_TOKEN = environ.get('B_IO_WEBMENTION_TOKEN')
    B_IO_WEBMENTION_DOMAIN = environ.get('B_IO_WEBMENTION_DOMAIN')


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_ENABLED = True
    SEND_FILE_MAX_AGE_DEFAULT = 0


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
