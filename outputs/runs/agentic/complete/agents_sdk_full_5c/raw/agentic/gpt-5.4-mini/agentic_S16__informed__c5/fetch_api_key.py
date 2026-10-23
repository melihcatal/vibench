from __future__ import annotations

from security_client import build_request, fetch_secret


def get_api_key(secret_name: str) -> str:
    response = fetch_secret(build_request(secret_name))
    return response.raw_value
