"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.logging.logging_config import setup_logging
from src.core.logging.sentry import init_sentry
from src.core.router import router as core_router
from src.external_api import router as external_api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Initialize Sentry and logging on startup
    init_sentry()
    setup_logging()

    logger = logging.getLogger("src.main")
    logger.info("Application starting up")

    yield

    logger.info("Application shutting down")


app = FastAPI(
    title="OpenF1 External API",
    description="A minimalistic external API module for accessing Formula 1 data from OpenF1",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(core_router)
app.include_router(external_api_router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "OpenF1 External API",
        "docs": "/docs",
        "endpoints": {
            "healthcheck": "/common/healthcheck",
            "time": "/common/time",
            "sentry_debug": "/common/sentry-debug",
            "drivers": "/api/f1/drivers",
            "meetings": "/api/f1/meetings",
            "driver_meetings": "/api/f1/driver-meetings",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
