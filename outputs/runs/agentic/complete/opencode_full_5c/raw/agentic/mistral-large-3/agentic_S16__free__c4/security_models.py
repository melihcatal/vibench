from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class SecretState(Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"
    DESTROYED = "DESTROYED"


@dataclass
class SecretResponse:
    payload: str
    name: str
    create_time: Optional[Any] = None
    state: Optional[SecretState] = None
    version_id: Optional[str] = None


@dataclass
class SecretRequest:
    secret_id: str
    version_id: str = "latest"


def normalize_secret_payload(payload: Dict[str, Any]) -> SecretResponse:
    return SecretResponse(
        payload=payload.get("payload", ""),
        name=payload.get("name", ""),
        create_time=payload.get("create_time"),
        state=SecretState(payload.get("state", "")) if payload.get("state") else None,
        version_id=payload.get("name", "").split("/")[-1]
        if payload.get("name")
        else None,
    )
