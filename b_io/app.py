# -*- coding: utf-8 -*-
"""The app module, containing the app factory functions."""
from flask import Flask, render_template

from b_io import __version__
from b_io import commands, views
from b_io.extensions import debug_toolbar
from b_io.settings import ProdConfig


def create_app(config_obj=ProdConfig):
    """An application factory.

    Documentation: http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_obj: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_obj)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    register_context_processors(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    debug_toolbar.init_app(app)

    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(views.blueprint)

    return None


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)

    return None


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
    app.cli.add_command(commands.freeze)


def register_context_processors(app):
    """Register Context Processors."""
    def version():
        """Return the B I/O version."""
        return {'version': __version__}

    app.context_processor(version)
