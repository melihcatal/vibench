import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SecretRequest:
    name: str
    version: Optional[str] = None
    stage: Optional[str] = None


@dataclass
class SecretResponse:
    name: str
    value: str
    version: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


def normalize_secret_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, bytes):
        return value.decode()
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def parse_json_secret(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return value
    text = normalize_secret_value(value)
    return json.loads(text)
