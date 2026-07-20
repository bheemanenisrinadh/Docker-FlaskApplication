"""
Health check endpoints, useful for Docker HEALTHCHECK and
orchestrator liveness/readiness probes.
"""
from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/healthz")
def healthz():
    """Liveness probe: process is up and able to respond."""
    return jsonify(status="ok"), 200


@health_bp.route("/readyz")
def readyz():
    """Readiness probe: add real checks here (DB, cache, etc.) as needed."""
    checks = {"app": "ok"}
    healthy = all(v == "ok" for v in checks.values())
    return jsonify(status="ok" if healthy else "degraded", checks=checks), (
        200 if healthy else 503
    )
