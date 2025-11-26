"""Tests for external API endpoints."""

from unittest.mock import AsyncMock, patch

import pytest

from src.external_api.dtos import DriverDTO, DriverMeetingDTO, MeetingDTO


@pytest.fixture
def mock_driver():
    return DriverDTO(
        driver_number=1,
        broadcast_name="M VERSTAPPEN",
        full_name="Max VERSTAPPEN",
        name_acronym="VER",
        team_name="Red Bull Racing",
        team_colour="0600EF",
        first_name="Max",
        last_name="Verstappen",
        headshot_url="http://example.com/max.png",
        country_code="NED",
        session_key=9158,
        meeting_key=1219,
    )


@pytest.fixture
def mock_meeting():
    return MeetingDTO(
        meeting_name="Bahrain Grand Prix",
        meeting_official_name="FORMULA 1 GULF AIR BAHRAIN GRAND PRIX 2024",
        location="Sakhir",
        country_key=36,
        country_code="BRN",
        country_name="Bahrain",
        circuit_key=63,
        circuit_short_name="Sakhir",
        date_start="2024-02-29T11:30:00",
        gmt_offset="03:00:00",
        meeting_key=1219,
        year=2024,
    )


def test_get_drivers_success(client, mock_driver):
    """Test getting drivers from external API."""
    with patch("src.external_api.service.service.get_drivers", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = [mock_driver]

        response = client.get("/api/f1/drivers?session_key=9158")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 1
        assert response.json()[0]["driver_number"] == 1


def test_get_meetings_success(client, mock_meeting):
    """Test getting meetings from external API."""
    with patch("src.external_api.service.service.get_meetings", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = [mock_meeting]

        response = client.get("/api/f1/meetings?year=2024")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 1
        assert response.json()[0]["meeting_key"] == 1219


def test_get_driver_meetings_success(client, mock_driver, mock_meeting):
    """Test getting combined driver-meetings data."""
    with patch("src.external_api.service.service.get_driver_with_meeting", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = [DriverMeetingDTO(driver=mock_driver, meeting=mock_meeting)]

        response = client.get("/api/f1/driver-meetings?session_key=9158")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 1
        assert response.json()[0]["driver"]["driver_number"] == 1
        assert response.json()[0]["meeting"]["meeting_key"] == 1219


def test_get_drivers_with_params(client, mock_driver):
    """Test getting drivers with query parameters."""
    with patch("src.external_api.service.service.get_drivers", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = [mock_driver]

        response = client.get("/api/f1/drivers?session_key=9158&driver_number=1")
        assert response.status_code == 200

        # Verify service was called with correct params
        mock_get.assert_called_with(session_key=9158, driver_number=1)


def test_get_meetings_with_country(client, mock_meeting):
    """Test getting meetings filtered by country."""
    with patch("src.external_api.service.service.get_meetings", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = [mock_meeting]

        response = client.get("/api/f1/meetings?country_name=Bahrain")
        assert response.status_code == 200

        # Verify service was called with correct params
        mock_get.assert_called_with(year=None, country_name="Bahrain", meeting_key=None)


@pytest.mark.asyncio
async def test_get_drivers_handles_api_error(client):
    """Test that driver endpoint handles external API errors."""
    with patch("src.external_api.service.service.get_drivers", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = Exception("API Error")

        response = client.get("/api/f1/drivers")
        assert response.status_code == 500


@pytest.mark.asyncio
async def test_get_meetings_handles_api_error(client):
    """Test that meetings endpoint handles external API errors."""
    with patch("src.external_api.service.service.get_meetings", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = Exception("API Error")

        response = client.get("/api/f1/meetings")
        assert response.status_code == 500
