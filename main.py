"""FastAPI application entry point."""

from fastapi import FastAPI
from external_api import router

app = FastAPI(
    title="OpenF1 External API",
    description="A minimalistic external API module for accessing Formula 1 data from OpenF1",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "OpenF1 External API",
        "docs": "/docs",
        "endpoints": {
            "drivers": "/api/f1/drivers",
            "meetings": "/api/f1/meetings",
            "driver_meetings": "/api/f1/driver-meetings"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
