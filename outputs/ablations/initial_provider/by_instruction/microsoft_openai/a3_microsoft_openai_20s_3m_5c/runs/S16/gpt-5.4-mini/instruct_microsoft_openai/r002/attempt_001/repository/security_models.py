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


def normalize_secret_payload(payload: Any) -> Dict[str, Any]:
    if hasattr(payload, "value"):
        return {"name": getattr(payload, "name", ""), "value": payload.value, "version": getattr(payload, "properties", None) and getattr(payload.properties, "version", None)}
    if isinstance(payload, dict):
        return payload
    return {"value": str(payload)}
