import json
from dataclasses import dataclass
from typing import Any


@dataclass
class SecretFetchRequest:
    secret_id: str


@dataclass
class RotationRequest:
    secret_id: str
    version_stage: str | None = None


def parse_secret_payload(payload: str) -> dict[str, Any]:
    try:
        data = json.loads(payload)
        return data if isinstance(data, dict) else {"value": data}
    except json.JSONDecodeError:
        return {"value": payload}


def normalize_connection_secret(payload: str) -> dict[str, str]:
    data = parse_secret_payload(payload)
    return {
        "host": str(data.get("host", "")),
        "port": str(data.get("port", "")),
        "username": str(data.get("username", data.get("user", ""))),
        "password": str(data.get("password", "")),
        "database": str(data.get("database", data.get("dbname", ""))),
    }
