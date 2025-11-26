"""Service layer for interacting with OpenF1 API."""

import logging
from typing import List, Optional

import httpx
import sentry_sdk

from .config import config
from .dtos import DriverDTO, DriverMeetingDTO, MeetingDTO

logger = logging.getLogger(__name__)


class OpenF1Service:
    """Service class for fetching data from OpenF1 API."""

    def __init__(self):
        """Initialize the service with HTTP client."""
        self.base_url = config.api_url
        self.timeout = config.REQUEST_TIMEOUT

    async def get_drivers(
        self, session_key: Optional[int] = None, driver_number: Optional[int] = None
    ) -> List[DriverDTO]:
        """Fetch drivers from OpenF1 API.

        Args:
            session_key: Optional session identifier to filter drivers
            driver_number: Optional driver number to filter by specific driver

        Returns:
            List of DriverDTO objects
        """
        url = f"{self.base_url}/drivers"
        params = {}

        if session_key is not None:
            params["session_key"] = session_key
        if driver_number is not None:
            params["driver_number"] = driver_number

        logger.info(f"[SERVICE][GET_DRIVERS] Calling OpenF1 API - url={url}, params={params}")

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

            logger.info(f"[SERVICE][GET_DRIVERS] Received {len(data)} drivers from API")
            return [DriverDTO(**item) for item in data]
        except Exception as e:
            logger.exception("[SERVICE][GET_DRIVERS] Error calling OpenF1 API")
            sentry_sdk.capture_exception(e)
            raise

    async def get_meetings(
        self, year: Optional[int] = None, country_name: Optional[str] = None, meeting_key: Optional[int] = None
    ) -> List[MeetingDTO]:
        """Fetch meetings from OpenF1 API.

        Args:
            year: Optional year to filter meetings
            country_name: Optional country name to filter by location
            meeting_key: Optional meeting key to get specific meeting

        Returns:
            List of MeetingDTO objects
        """
        url = f"{self.base_url}/meetings"
        params = {}

        if year is not None:
            params["year"] = year
        if country_name is not None:
            params["country_name"] = country_name
        if meeting_key is not None:
            params["meeting_key"] = meeting_key

        logger.info(f"[SERVICE][GET_MEETINGS] Calling OpenF1 API - url={url}, params={params}")

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

            logger.info(f"[SERVICE][GET_MEETINGS] Received {len(data)} meetings from API")
            return [MeetingDTO(**item) for item in data]
        except Exception as e:
            logger.exception("[SERVICE][GET_MEETINGS] Error calling OpenF1 API")
            sentry_sdk.capture_exception(e)
            raise

    async def get_driver_with_meeting(
        self, session_key: Optional[int] = None, driver_number: Optional[int] = None
    ) -> List[DriverMeetingDTO]:
        """Fetch drivers with their associated meeting information.

        This method combines data from both drivers and meetings endpoints.

        Args:
            session_key: Optional session identifier to filter drivers
            driver_number: Optional driver number to filter by specific driver

        Returns:
            List of DriverMeetingDTO objects (combined data)
        """
        logger.info("[SERVICE][GET_DRIVER_WITH_MEETING] Combining driver and meeting data")

        drivers = await self.get_drivers(session_key=session_key, driver_number=driver_number)

        if not drivers:
            logger.info("[SERVICE][GET_DRIVER_WITH_MEETING] No drivers found")
            return []

        result = []
        for driver in drivers:
            meetings = await self.get_meetings(meeting_key=driver.meeting_key)
            if meetings:
                combined = DriverMeetingDTO(driver=driver, meeting=meetings[0])
                result.append(combined)

        logger.info(f"[SERVICE][GET_DRIVER_WITH_MEETING] Combined {len(result)} driver-meeting records")
        return result


service = OpenF1Service()
