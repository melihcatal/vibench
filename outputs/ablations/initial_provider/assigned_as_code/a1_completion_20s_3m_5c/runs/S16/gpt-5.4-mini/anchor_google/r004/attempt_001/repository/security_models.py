import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SecretRequest:
    secret_id: str
    key_field: Optional[str] = None
    version: str = "latest"


@dataclass
class SecretResponse:
    value: Any


def normalize_secret_payload(value: str) -> Any:
    try:
        return json.loads(value)
    except Exception:
        return value


def select_key_field(value: Any, key_field: Optional[str]) -> Any:
    if key_field and isinstance(value, dict):
        return value[key_field]
    return value


def as_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {"value": value}
