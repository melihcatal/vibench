import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SecretFetchRequest:
    secret_id: str
    version_id: str = "latest"


@dataclass
class SecretFetchResponse:
    secret_id: str
    version_id: str
    value: str


def normalize_json_secret(value: str) -> Dict[str, Any]:
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError("JSON secret must decode to an object")
    return parsed


def normalize_label_text(value: Optional[str]) -> str:
    if value is None:
        return ""
    return " ".join(value.strip().split())
