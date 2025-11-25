"""FastAPI router for external API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException

from .dtos import DriverDTO, MeetingDTO, DriverMeetingDTO
from .service import service
from .config import config

router = APIRouter(prefix="/api/f1", tags=["Formula 1"])


@router.get("/drivers", response_model=List[DriverDTO])
async def get_drivers(
    session_key: Optional[int] = Query(
        None,
        description=f"Session key to filter drivers (default: {config.DEFAULT_SESSION_KEY})"
    ),
    driver_number: Optional[int] = Query(
        None,
        description="Driver number to filter by specific driver"
    )
) -> List[DriverDTO]:
    """Get Formula 1 drivers information.
    
    Fetches driver data from OpenF1 API. You can filter by session and/or driver number.
    """
    try:
        # Use default session key if none provided
        if session_key is None and driver_number is not None:
            session_key = config.DEFAULT_SESSION_KEY
            
        drivers = await service.get_drivers(
            session_key=session_key,
            driver_number=driver_number
        )
        return drivers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching drivers: {str(e)}")


@router.get("/meetings", response_model=List[MeetingDTO])
async def get_meetings(
    year: Optional[int] = Query(
        None,
        description=f"Year to filter meetings (default: {config.DEFAULT_YEAR})"
    ),
    country_name: Optional[str] = Query(
        None,
        description="Country name to filter meetings by location"
    ),
    meeting_key: Optional[int] = Query(
        None,
        description="Meeting key to get specific meeting"
    )
) -> List[MeetingDTO]:
    """Get Formula 1 meetings (Grand Prix) information.
    
    Fetches meeting data from OpenF1 API. You can filter by year, country, or meeting key.
    """
    try:
        # Use default year if no filters provided
        if year is None and country_name is None and meeting_key is None:
            year = config.DEFAULT_YEAR
            
        meetings = await service.get_meetings(
            year=year,
            country_name=country_name,
            meeting_key=meeting_key
        )
        return meetings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching meetings: {str(e)}")


@router.get("/driver-meetings", response_model=List[DriverMeetingDTO])
async def get_driver_meetings(
    session_key: Optional[int] = Query(
        config.DEFAULT_SESSION_KEY,
        description=f"Session key to filter drivers (default: {config.DEFAULT_SESSION_KEY})"
    ),
    driver_number: Optional[int] = Query(
        None,
        description="Driver number to filter by specific driver"
    )
) -> List[DriverMeetingDTO]:
    """Get combined driver and meeting information.
    
    Fetches drivers along with their associated Grand Prix meeting data.
    This endpoint combines data from both /drivers and /meetings endpoints.
    """
    try:
        combined_data = await service.get_driver_with_meeting(
            session_key=session_key,
            driver_number=driver_number
        )
        return combined_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching driver meetings: {str(e)}")
