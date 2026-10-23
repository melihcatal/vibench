from __future__ import annotations

from typing import Any

from security_client import access_secret_version, get_default_locator


def parse_json_secret(secret_id: str, version_id: str = "latest") -> dict[str, Any]:
    locator = get_default_locator(secret_id=secret_id, version_id=version_id)
    response = access_secret_version(locator)
    return __import__("json").loads(response.payload.data.decode("utf-8"))
