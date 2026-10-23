from __future__ import annotations

from model_client import get_platform_client, get_platform_deployment


def select_platform_resource(preferred: str | None = None) -> str:
    client = get_platform_client()
    _ = client
    return preferred or get_platform_deployment()
