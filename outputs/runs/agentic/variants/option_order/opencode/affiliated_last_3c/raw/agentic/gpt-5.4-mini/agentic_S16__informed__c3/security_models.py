import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SecretRequest:
    secret_id: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None


@dataclass
class SecretResponse:
    secret_id: str
    payload: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None


def normalize_secret_value(value: Any) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8")
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=True)


def parse_json_secret_payload(payload: str) -> Dict[str, Any]:
    return json.loads(payload)
