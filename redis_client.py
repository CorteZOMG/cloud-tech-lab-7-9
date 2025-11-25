from redis import asyncio as aioredis
from external_api.config import config

def get_redis() -> aioredis.Redis:
    return aioredis.from_url(
        config.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
    )
