"""
Redis Client
============
Async Redis connection management with connection pooling.
"""
from typing import Any, Optional
import redis.asyncio as redis
from config import get_settings

# Global Redis client
_redis_client: Optional[redis.Redis] = None


async def get_redis_client() -> redis.Redis:
    """Get or create Redis client."""
    global _redis_client

    if _redis_client is None:
        settings = get_settings()
        _redis_client = redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
            max_connections=settings.redis_max_connections,
        )

    return _redis_client


async def close_redis_client() -> None:
    """Close Redis connection."""
    global _redis_client

    if _redis_client:
        await _redis_client.close()
        _redis_client = None


class RedisCache:
    """Redis-backed cache with TTL support."""

    def __init__(self, client: redis.Redis, prefix: str = "clarix:"):
        self.client = client
        self.prefix = prefix

    def _key(self, key: str) -> str:
        """Add prefix to key."""
        return f"{self.prefix}{key}"

    async def get(self, key: str) -> Optional[str]:
        """Get value from cache."""
        return await self.client.get(self._key(key))

    async def set(
        self,
        key: str,
        value: str,
        ttl: Optional[int] = None,
    ) -> None:
        """Set value in cache with optional TTL."""
        if ttl:
            await self.client.setex(self._key(key), ttl, value)
        else:
            await self.client.set(self._key(key), value)

    async def delete(self, key: str) -> None:
        """Delete key from cache."""
        await self.client.delete(self._key(key))

    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        return await self.client.exists(self._key(key)) > 0

    async def incr(self, key: str, amount: int = 1) -> int:
        """Increment counter."""
        return await self.client.incr(self._key(key), amount)

    async def expire(self, key: str, ttl: int) -> None:
        """Set TTL on key."""
        await self.client.expire(self._key(key), ttl)


class RedisQueue:
    """Redis-backed queue for async task processing."""

    def __init__(self, client: redis.Redis, queue_name: str = "default"):
        self.client = client
        self.queue_name = f"clarix:queue:{queue_name}"

    async def enqueue(self, *values: str) -> None:
        """Add items to queue."""
        await self.client.rpush(self.queue_name, *values)

    async def dequeue(self, timeout: int = 0) -> Optional[str]:
        """Remove and return item from queue."""
        if timeout > 0:
            result = await self.client.blpop(self.queue_name, timeout=timeout)
            return result[1] if result else None
        return await self.client.lpop(self.queue_name)

    async def queue_size(self) -> int:
        """Get queue size."""
        return await self.client.llen(self.queue_name)

    async def clear(self) -> None:
        """Clear the queue."""
        await self.client.delete(self.queue_name)
