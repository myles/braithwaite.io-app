# -*- coding: utf-8 -*-
"""Extensions module.

Each extension is initialized in the app factory located in app.py.
"""
from flask_debugtoolbar import DebugToolbarExtension
from flask_webpack import Webpack

debug_toolbar = DebugToolbarExtension()
webpack = Webpack()
