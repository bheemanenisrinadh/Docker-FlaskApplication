"""
Main application routes.
"""
from flask import Blueprint, jsonify, render_template, request

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Render the home page."""
    return render_template("index.html", title="Flask Starter")


@main_bp.route("/about")
def about():
    """Render a simple about page."""
    return render_template("about.html", title="About")


@main_bp.route("/api/echo", methods=["POST"])
def echo():
    """Example JSON API endpoint: echoes back posted JSON."""
    data = request.get_json(silent=True) or {}
    return jsonify(received=data), 200


@main_bp.errorhandler(404)
def not_found(_error):
    return render_template("404.html", title="Not Found"), 404
