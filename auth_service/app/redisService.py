import json
from typing import Any, Optional

import redis.asyncio as redis


class AsyncRedis:
    def __init__(self, redis_url: str = "redis://redis:6379/0"):
        self.redis_url = redis_url
        self.redis = None

    async def connect(self):
        """Establish connection to Redis"""
        self.redis = redis.from_url(self.redis_url, decode_responses=True)
        return self

    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Set a key with optional expiration (seconds)"""
        serialized = json.dumps(value)
        if expire:
            return await self.redis.setex(key, expire, serialized)
        else:
            return await self.redis.set(key, serialized)

    async def get(self, key: str) -> Optional[Any]:
        """Get a value by key"""
        value = await self.redis.get(key)
        return json.loads(value) if value else None

    async def delete(self, key: str) -> bool:
        """Delete a key"""
        return await self.redis.delete(key) > 0

    async def exists(self, key: str) -> bool:
        """Check if a key exists"""
        return await self.redis.exists(key) > 0

    async def close(self):
        """Close the connection"""
        await self.redis.close()
