from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SecretRequest:
    name: str
    version: Optional[str] = None
    stage: Optional[str] = None


@dataclass
class SecretValue:
    name: str
    value: Any
    version: Optional[str] = None
    stage: Optional[str] = None


def normalize_secret_payload(payload: Any) -> Any:
    if isinstance(payload, dict) and "value" in payload and len(payload) == 1:
        return payload["value"]
    return payload


def secret_to_dict(secret: SecretValue) -> Dict[str, Any]:
    return {"name": secret.name, "value": secret.value, "version": secret.version, "stage": secret.stage}
