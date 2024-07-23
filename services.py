import asyncio
import aioredis
from config import REDIS_HOST, REDIS_PORT
class RedisService:
    def __init__(self):
        self.redis = None
    async def connect(self):
        self.redis = await aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
    async def close(self):
        if self.redis:
            await self.redis.close()
    async def set(self, key, value):
        if self.redis:
            await self.redis.set(key, value)
    async def get(self, key):
        if self.redis:
            return await self.redis.get(key)