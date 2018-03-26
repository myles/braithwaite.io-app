# -*- coding: utf-8 -*-
"""Create a Flask application instance."""
from flask.helpers import get_debug_flag

from b_io.app import create_app
from b_io.settings import DevConfig, ProdConfig

Config = DevConfig if get_debug_flag() else ProdConfig

app = create_app(Config)
