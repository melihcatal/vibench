import json
from dataclasses import dataclass
from typing import Any


@dataclass
class SecretFetchResult:
    name: str
    value: Any


def coerce_text_secret(payload: str) -> str:
    return payload.strip()


def normalize_db_secret(payload: str) -> dict[str, Any]:
    data = json.loads(payload)
    return {
        'username': data.get('username', ''),
        'password': data.get('password', ''),
        'host': data.get('host', ''),
        'port': data.get('port', 5432),
        'database': data.get('database', ''),
    }


def parse_json_payload(payload: str) -> dict[str, Any]:
    return json.loads(payload)
