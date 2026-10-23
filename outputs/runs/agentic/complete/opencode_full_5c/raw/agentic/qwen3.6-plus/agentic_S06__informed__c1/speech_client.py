import os
import httpx
from typing import Optional


ELEVENLABS_API_BASE = "https://api.elevenlabs.io/v1"


def get_elevenlabs_api_key() -> str:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is not set")
    return api_key


def build_headers(api_key: Optional[str] = None) -> dict:
    key = api_key or get_elevenlabs_api_key()
    return {
        "xi-api-key": key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }


def build_json_headers(api_key: Optional[str] = None) -> dict:
    key = api_key or get_elevenlabs_api_key()
    return {
        "xi-api-key": key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def create_client(
    api_key: Optional[str] = None, timeout: float = 120.0
) -> httpx.Client:
    key = api_key or get_elevenlabs_api_key()
    return httpx.Client(
        base_url=ELEVENLABS_API_BASE,
        headers={"xi-api-key": key},
        timeout=timeout,
    )


def create_async_client(
    api_key: Optional[str] = None, timeout: float = 120.0
) -> httpx.AsyncClient:
    key = api_key or get_elevenlabs_api_key()
    return httpx.AsyncClient(
        base_url=ELEVENLABS_API_BASE,
        headers={"xi-api-key": key},
        timeout=timeout,
    )
