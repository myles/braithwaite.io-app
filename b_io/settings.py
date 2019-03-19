from os import environ
from pathlib import Path


class Config:
    """Base configuration."""

    SECRET_KEY = environ.get("B_IO_SECRET", "secret-key")

    PROJECT_ROOT = Path(__file__).parents[1]
    APP_DIR = Path(__file__).parents[0]

    STATIC_FOLDER = APP_DIR / "static"
    TEMPLATES_FOLDER = APP_DIR / "templates"
    CONTENT_ROOT = environ.get(
        "B_IO_CONTENT_PATH", PROJECT_ROOT / "content"
    )

    GITHUB_REPO = environ.get(
        "B_IO_GITHUB_REPO", "https://github.com/myles/braithwaite.io-notebook"
    )

    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    FREEZER_DESTINATION = environ.get(
        "B_IO_BUILD_PATH", PROJECT_ROOT / "build"
    )
    FREEZER_IGNORE_MIMETYPE_WARNINGS = True

    WEBPACK_MANIFEST_PATH = STATIC_FOLDER / "manifest.json"
    WEBPACK_ASSETS_URL = "/static/"

    WEBMENTION_TOKEN = environ.get("B_IO_WEBMENTION_TOKEN")
    B_IO_WEBMENTION_DOMAIN = environ.get("B_IO_WEBMENTION_DOMAIN")

    SENTRY_DSN = None


class ProdConfig(Config):
    """Production configuration."""

    ENV = "prod"
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar

    SENTRY_DSN = environ.get("B_IO_SENTRY_DSN")


class DevConfig(Config):
    """Development configuration."""

    ENV = "dev"
    DEBUG = True
    DEBUG_TB_ENABLED = True
    SEND_FILE_MAX_AGE_DEFAULT = 0


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
