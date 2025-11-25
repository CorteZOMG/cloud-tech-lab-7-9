from fastapi import APIRouter, HTTPException
from redis_client import get_redis

router = APIRouter(prefix="/cache", tags=["Redis Cache"])

@router.post("/set")
async def set_cache(key: str, value: str):
    redis = get_redis()
    await redis.set(key, value)
    await redis.close()
    return {"message": "Value set successfully", "key": key, "value": value}

@router.get("/get/{key}")
async def get_cache(key: str):
    redis = get_redis()
    value = await redis.get(key)
    await redis.close()
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": value}
