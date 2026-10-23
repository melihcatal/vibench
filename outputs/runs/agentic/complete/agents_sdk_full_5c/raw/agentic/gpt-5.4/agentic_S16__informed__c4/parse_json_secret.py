from __future__ import annotations

from typing import Any, Dict

from security_client import build_secrets_manager_client
from security_models import normalize_secret_value, parse_json_secret_value


def parse_json_secret(secret_id: str, region_name: str | None = None) -> Dict[str, Any]:
    client = build_secrets_manager_client(region_name)
    response = client.get_secret_value(SecretId=secret_id, VersionStage="AWSCURRENT")
    payload = normalize_secret_value(secret_id, response)
    return parse_json_secret_value(payload)
