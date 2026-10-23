from dataclasses import dataclass
from typing import Any, Dict, Optional
import json


def normalize_secret_value(value: Any) -> Any:
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return value


def parse_json_payload(value: Any) -> Dict[str, Any]:
    value = normalize_secret_value(value)
    if isinstance(value, dict):
        return value
    if value is None:
        return {}
    return json.loads(value)


@dataclass
class SecretRequest:
    secret_id: str
    version_stage: Optional[str] = None
    version_id: Optional[str] = None


@dataclass
class SecretResponse:
    secret_id: str
    value: Any
    version_id: Optional[str] = None
    version_stage: Optional[str] = None
