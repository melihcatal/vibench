from __future__ import annotations

from security_client import fetch_secret_payload
from security_models import parse_json_secret_value


def fetch_db_secret(secret_id: str) -> dict:
    payload = fetch_secret_payload(secret_id)
    data = parse_json_secret_value(payload.value)
    return {
        "provider": "aws-secrets-manager",
        "secret_id": payload.secret_id,
        "version_id": payload.version_id,
        "engine": data.get("engine"),
        "host": data.get("host"),
        "port": data.get("port"),
        "username": data.get("username"),
        "password": data.get("password"),
        "dbname": data.get("dbname") or data.get("database"),
    }
