from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_secret_payload(payload: Any) -> Dict[str, Any]:
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        return {"secret_string": payload}
    return {"value": payload}


@dataclass
class SecretRequest:
    secret_id: str
    version_stage: Optional[str] = None
    version_id: Optional[str] = None


@dataclass
class SecretResponse:
    secret_id: str
    payload: Dict[str, Any]
    version_stage: Optional[str] = None
    version_id: Optional[str] = None


def coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)
