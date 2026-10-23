from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_secret_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if payload is None:
        return {}
    return {"value": payload}


@dataclass
class SecretRequest:
    secret_id: str
    version: Optional[str] = None
    stage: Optional[str] = None


@dataclass
class SecretResponse:
    secret_id: str
    version: Optional[str]
    payload: Dict[str, Any]
