import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app("testing")
    return app.test_client()


def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Flask Starter Template" in resp.data


def test_about(client):
    resp = client.get("/about")
    assert resp.status_code == 200


def test_404(client):
    resp = client.get("/does-not-exist")
    assert resp.status_code == 404


def test_echo(client):
    resp = client.post("/api/echo", json={"hello": "world"})
    assert resp.status_code == 200
    assert resp.get_json() == {"received": {"hello": "world"}}


def test_healthz(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_readyz(client):
    resp = client.get("/readyz")
    assert resp.status_code == 200
