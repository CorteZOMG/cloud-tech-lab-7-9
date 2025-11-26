"""pytest configuration and fixtures."""

import os

import pytest
from fastapi.testclient import TestClient

from src.main import app

# Set testing environment variable
os.environ["TESTING"] = "1"


@pytest.fixture(scope="session")
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)
