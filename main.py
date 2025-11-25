"""FastAPI application entry point."""

from fastapi import FastAPI
from external_api.router import router as f1_router
from user_router import router as user_router
from redis_router import router as redis_router

app = FastAPI(
    title="Cloud Tech Lab 7-9 & 10-15",
    description="API for Formula 1 data with PostgreSQL and Redis integration",
    version="1.0.0"
)

app.include_router(f1_router)
app.include_router(user_router)
app.include_router(redis_router)


@app.get("/")
async def root():
    return {
        "message": "Cloud Tech Lab 7-9 & 10-15 API",
        "docs": "/docs",
        "endpoints": {
            "drivers": "/api/f1/drivers",
            "meetings": "/api/f1/meetings",
            "driver_meetings": "/api/f1/driver-meetings",
            "users": "/users",
            "cache": "/cache"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
