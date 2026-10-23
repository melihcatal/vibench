import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SecretRequest:
    secret_id: str
    version_stage: Optional[str] = None
    version_id: Optional[str] = None


@dataclass
class SecretResponse:
    secret_id: str
    secret_string: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None


def normalize_secret_string(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8")
    if isinstance(value, str):
        return value
    return json.dumps(value, separators=(",", ":"), sort_keys=True)


def parse_json_secret(value: str) -> Dict[str, Any]:
    return json.loads(value)
