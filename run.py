"""
Local development entrypoint. Do NOT use this in the container;
use gunicorn + wsgi:app there instead (see README).
"""
import os

from app import create_app

if __name__ == "__main__":
    app = create_app(os.environ.get("FLASK_ENV", "development"))
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
