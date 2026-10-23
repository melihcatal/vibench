from __future__ import annotations

from typing import Any, Dict

from security_client import build_request, fetch_secret


def get_db_secret(secret_name: str) -> Dict[str, Any]:
    response = fetch_secret(build_request(secret_name))
    parsed = response.parsed
    if isinstance(parsed, dict):
        return parsed
    return {"secret": response.raw_value}
