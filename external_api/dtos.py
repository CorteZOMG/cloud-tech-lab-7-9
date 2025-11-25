"""Data Transfer Objects for OpenF1 API responses."""

from typing import Optional
from pydantic import BaseModel, Field


class DriverDTO(BaseModel):
    """DTO for driver information from OpenF1 API."""
    
    driver_number: int = Field(..., description="Driver's racing number")
    broadcast_name: str = Field(..., description="Name as shown on broadcast")
    full_name: str = Field(..., description="Full name of the driver")
    name_acronym: str = Field(..., description="Three-letter acronym")
    team_name: str = Field(..., description="Team the driver races for")
    team_colour: str = Field(..., description="Team color hex code")
    first_name: str = Field(..., description="Driver's first name")
    last_name: str = Field(..., description="Driver's last name")
    country_code: str = Field(..., description="Driver's country code")
    session_key: int = Field(..., description="Session identifier")
    meeting_key: int = Field(..., description="Meeting identifier")
    headshot_url: Optional[str] = Field(None, description="URL to driver's headshot")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class MeetingDTO(BaseModel):
    """DTO for meeting (Grand Prix) information from OpenF1 API."""
    
    meeting_key: int = Field(..., description="Unique meeting identifier")
    meeting_name: str = Field(..., description="Name of the Grand Prix")
    meeting_official_name: str = Field(..., description="Official full name")
    location: str = Field(..., description="Location of the meeting")
    country_name: str = Field(..., description="Country name")
    country_code: str = Field(..., description="Country code")
    circuit_key: int = Field(..., description="Circuit identifier")
    circuit_short_name: str = Field(..., description="Short name of the circuit")
    date_start: str = Field(..., description="Start date of the meeting")
    year: int = Field(..., description="Year of the meeting")
    gmt_offset: str = Field(..., description="GMT offset for the location")
    country_key: int = Field(..., description="Country identifier")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class DriverMeetingDTO(BaseModel):
    """Combined DTO joining driver with their meeting information."""
    
    driver: DriverDTO = Field(..., description="Driver information")
    meeting: MeetingDTO = Field(..., description="Meeting information")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True
