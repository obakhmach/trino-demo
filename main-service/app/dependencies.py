from redis.asyncio import Redis
from typing import Generator

from app.settings import settings


async def get_redis() -> Generator[Redis, None, None]:
    """A dependency needed to inject redis client connection
    in any place of the app.

    Returns:
        Returns nothing but yeiling a redis client.
    """
    redis_client_connection: Redis = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password,
    )

    yield redis_client_connection

    await redis_client_connection.close()
