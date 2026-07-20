"""
Application factory for the Flask starter app.
"""
import logging
import os

from flask import Flask

from config import get_config


def create_app(config_name: str | None = None) -> Flask:
    """Create and configure the Flask application.

    Args:
        config_name: Name of the config to load ("development", "production",
            "testing"). Falls back to the FLASK_ENV environment variable,
            then "production".

    Returns:
        A configured Flask application instance.
    """
    app = Flask(__name__)

    config_name = config_name or os.environ.get("FLASK_ENV", "production")
    app.config.from_object(get_config(config_name))

    _configure_logging(app)

    # Blueprints
    from app.routes import main_bp
    from app.health import health_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(health_bp)

    return app


def _configure_logging(app: Flask) -> None:
    level = logging.DEBUG if app.config.get("DEBUG") else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
    app.logger.setLevel(level)
