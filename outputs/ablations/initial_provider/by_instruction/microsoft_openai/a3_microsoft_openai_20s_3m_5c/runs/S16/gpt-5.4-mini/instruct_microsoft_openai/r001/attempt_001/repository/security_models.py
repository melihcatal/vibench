from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_secret_payload(payload: Any) -> Dict[str, Any]:
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    return {"value": payload}


@dataclass
class SecretRequest:
    secret_name: str
    version: Optional[str] = None
    stage: Optional[str] = None


@dataclass
class SecretResponse:
    name: str
    value: Any
    metadata: Dict[str, Any]


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()
