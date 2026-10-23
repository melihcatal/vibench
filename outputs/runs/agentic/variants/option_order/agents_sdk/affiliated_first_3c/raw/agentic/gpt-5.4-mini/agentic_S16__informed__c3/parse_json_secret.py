from __future__ import annotations

import json
import os

from security_client import fetch_json_secret


def parse_json_secret(secret_id: str | None = None) -> dict[str, object] | None:
    name = secret_id or os.getenv("SECURITY_JSON_SECRET_ID", "app/json-config")
    normalized = fetch_json_secret(name)
    if normalized.parsed_json is not None:
        return normalized.parsed_json
    return json.loads(normalized.text)
