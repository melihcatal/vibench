import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SecretRequest:
    project_id: str
    secret_name: str
    version: str = "latest"
    labels: Optional[Dict[str, str]] = None


@dataclass
class SecretResponse:
    name: str
    payload: Any
    raw: Any


def normalize_secret_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return str(value)


def parse_json_payload(value: Any) -> Dict[str, Any]:
    text = normalize_secret_text(value)
    if not text:
        return {}
    return json.loads(text)
