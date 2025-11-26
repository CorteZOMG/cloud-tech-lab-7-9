"""Tests for common routes."""

from unittest.mock import patch


def test_healthcheck(client):
    """Test healthcheck endpoint returns 200 OK."""
    response = client.get("/common/healthcheck")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "message" in response.json()


def test_time(client):
    """Test time endpoint returns server time."""
    response = client.get("/common/time")
    assert response.status_code == 200
    assert "server_time" in response.json()


def test_unknown_route_returns_404(client):
    """Test that unknown routes return 404."""
    response = client.get("/common/not-existing-route")
    assert response.status_code == 404


def test_healthcheck_wrong_method(client):
    """Test healthcheck with wrong HTTP method returns 405."""
    response = client.post("/common/healthcheck")
    assert response.status_code == 405


def test_time_internal_error(client):
    """Test time endpoint handles internal errors gracefully."""
    with patch("src.core.router.datetime.datetime") as mock_dt:
        mock_dt.now.side_effect = Exception("Internal error")

        response = client.get("/common/time")
        assert response.status_code == 500


def test_sentry_debug_endpoint(client):
    """Test sentry debug endpoint triggers an error."""
    response = client.get("/common/sentry-debug")
    assert response.status_code == 500
    assert "error" in response.json()["detail"].lower()
