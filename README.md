# Flask Starter

Generic, production-ready Flask starter: app factory pattern, blueprints,
environment-driven config, templates/static assets, health checks, and tests.

## Local development (without Docker)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
python run.py            # dev server on http://localhost:5000
pytest                    # run tests
```

## Structure

```
app/
  __init__.py       # create_app() factory
  routes.py         # main blueprint (/, /about, /api/echo)
  health.py         # health blueprint (/healthz, /readyz)
  templates/
  static/css/
config.py           # Development/Testing/Production config classes
wsgi.py             # gunicorn entrypoint: wsgi:app
run.py              # local-only dev server, NOT used in container
requirements.txt    # runtime deps
requirements-dev.txt
tests/
```

## What you need to know to write the Dockerfile

- **Entrypoint for the container**: use `wsgi.py` via gunicorn, not `run.py`
  (`run.py` is Flask's dev server — single-threaded, not for production).
  Run command: `gunicorn --bind 0.0.0.0:8000 --workers 3 wsgi:app`
- **Port**: app listens on `8000` inside the container (matches the `PORT`
  value in `.env.example`). Expose/publish that port.
- **Python version**: written for Python 3.11+ (no version-specific syntax
  beyond that), so `python:3.11-slim` or `python:3.12-slim` both work.
- **Dependencies**: install from `requirements.txt` only for the runtime
  image (skip `requirements-dev.txt` — that's for CI/local testing).
- **No native/system build dependencies** are required — Flask, gunicorn,
  and python-dotenv are pure-Python wheels, so no `apt-get` build tools are
  needed beyond a base slim image.
- **Environment variables the app reads** (set these at `docker run`/compose
  time, don't bake secrets into the image):
  - `FLASK_ENV` — `production` (default), `development`, or `testing`
  - `SECRET_KEY` — must be overridden in production
  - `PORT` — only used by `run.py`; irrelevant if gunicorn's `--bind` sets
    the port directly (recommended)
- **Static files**: served directly by Flask (`app/static/`) — fine for a
  starter template; for higher-traffic production use you'd typically add
  nginx or a CDN in front, but that's out of scope for this template.
- **Health checks**: `GET /healthz` (liveness) and `GET /readyz` (readiness)
  are already implemented — wire these into `HEALTHCHECK` in the Dockerfile
  or your orchestrator's probes.
- **Non-root user**: recommended to create and switch to a non-root user in
  the Dockerfile before running gunicorn.
- **.dockerignore** is already included in this repo, so build context stays
  small (excludes tests, venv, git, caches).
- **Multi-stage build**: optional but not necessary here since there's
  nothing to compile — a single-stage slim image is sufficient.

## Example run command once you have an image built

```bash
docker run -d -p 8000:8000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY="$(openssl rand -hex 32)" \
  --name flask-starter \
  your-image-name:tag
```
# Docker-FlaskApplication
