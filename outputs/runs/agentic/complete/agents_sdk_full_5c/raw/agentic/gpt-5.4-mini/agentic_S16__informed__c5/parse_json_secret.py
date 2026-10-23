from __future__ import annotations

from typing import Any

from security_client import build_request, fetch_secret


def get_parsed_json_secret(secret_name: str) -> Any:
    response = fetch_secret(build_request(secret_name))
    return response.parsed
