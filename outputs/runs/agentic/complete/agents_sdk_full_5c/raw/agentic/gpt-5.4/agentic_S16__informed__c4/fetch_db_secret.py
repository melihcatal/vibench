from __future__ import annotations

from typing import Any, Dict

from security_client import build_secrets_manager_client
from security_models import normalize_secret_value, parse_json_secret_value


REQUIRED_DB_FIELDS = {"host", "username", "password"}


def fetch_db_secret(secret_id: str, region_name: str | None = None) -> Dict[str, Any]:
    client = build_secrets_manager_client(region_name)
    response = client.get_secret_value(SecretId=secret_id, VersionStage="AWSCURRENT")
    payload = normalize_secret_value(secret_id, response)
    secret_data = parse_json_secret_value(payload)
    missing = sorted(REQUIRED_DB_FIELDS.difference(secret_data))
    if missing:
        raise ValueError(f"Database secret missing required fields: {', '.join(missing)}")
    return secret_data
