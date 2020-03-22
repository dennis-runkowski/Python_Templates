"""Main Flask app for the website and api."""
from flask import Flask
from flask_app.extensions import bootstrap, db, bcrypt, mail
import flask_app.views as views
import logging
from custom_pkg import get_config

CONFIG = get_config()

def setup_config():
    """
    Helper function to configure environment based on config.
    """
    if CONFIG.get("environment", "server") == 'production':
        return 'config.ProductionConfig'
    else:
        return 'config.TestingConfig'


def create_app():
    """Main application factory."""
    app = Flask(__name__)

    # Use helper function to source environment from config
    environment = setup_config()
    app.config.from_object(environment)

    # Setup logging level
    if environment == 'config.ProductionConfig':
        logging.basicConfig(level=logging.WARN)
    else:
        logging.basicConfig(level=logging.DEBUG)

    register_extensions(app)
    register_blueprints(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app


def register_extensions(app):
    """Register flask extensions."""
    bootstrap.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)


def register_blueprints(app):
    """Register flask blueprints."""
    app.register_blueprint(views.home_blueprint)


def register_errors(app):
    """Register flask error handling."""
    # TODO
    pass
