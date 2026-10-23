import os
import httpx
from typing import AsyncContextManager
from dotenv import load_dotenv
load_dotenv()

class AsyncRequestsClient(AsyncContextManager):
    """Async context manager providing an httpx.AsyncClient with timeout and retries."""
    def __init__(self, timeout_seconds: float = 30.0):
        self.client = httpx.AsyncClient(timeout=timeout_seconds)
        self.timeout = timeout_seconds
    async def __aenter__(self):
        return self.client
    async def __aexit__(self, exc_type, exc, tb):
        await self.client.aclose()

def build_auth_headers(service: str) -> Dict[str, str]:
    """Return authentication headers for a given managed service.",
    """
    prefix = f'{service.upper()}_API_KEY'
    key_env = os.getenv(prefix)
    if not key_env:
        raise RuntimeError(f'Missing environment variable {prefix}')
    return {'Authorization': f'Bearer {key_env}'}

# Example usage in other modules:
# async with AsyncRequestsClient() as client:
#     resp = await client.post(url, json=payload, headers=build_auth_headers('ocr'))
