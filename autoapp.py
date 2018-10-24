# -*- coding: utf-8 -*-
"""Create a Flask application instance."""
import sentry_sdk
from flask.helpers import get_debug_flag
from sentry_sdk.integrations.flask import FlaskIntegration

from b_io.app import create_app
from b_io.settings import DevConfig, ProdConfig

Config = DevConfig if get_debug_flag() else ProdConfig

if Config.SENTRY_DSN:
    sentry_sdk.init(dsn=Config.SENTRY_DSN, integrations=[FlaskIntegration()])

app = create_app(Config)
