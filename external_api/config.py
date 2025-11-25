import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class OpenF1Config:
    """Configuration for OpenF1 API client.
    
    This dataclass contains all magic numbers and configuration constants
    used throughout the external_api module.
    """
    
    BASE_URL: str = "https://api.openf1.org"
    API_VERSION: str = "v1"
    
    # Magic Numbers
    REQUEST_TIMEOUT: int = 30  # seconds
    DEFAULT_SESSION_KEY: int = 9158  # Singapore 2023 GP qualifying session
    DEFAULT_YEAR: int = 2023
    MAX_RETRIES: int = 3
    
    # Database & Redis
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_TTL: int = 60

    @property
    def api_url(self) -> str:
        """Construct the full API URL."""
        return f"{self.BASE_URL}/{self.API_VERSION}"

config = OpenF1Config()
