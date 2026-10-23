import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SecretRequest:
    name: str
    version: Optional[str] = None


@dataclass
class SecretResponse:
    name: str
    value: str
    version: Optional[str] = None


def parse_json_secret(value: str) -> Dict[str, Any]:
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError("Secret JSON must decode to an object")
    return parsed


def normalize_secret_name(name: str) -> str:
    return name.strip()
