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
    version: str
    create_time: str
    state: SecretState
    labels: Optional[Dict[str, str]] = None
    notes: Optional[str] = None


@dataclass
class SecretRotationSummary:
    secret_id: str
    current_version: str
    previous_version: Optional[str]
    rotation_time: str
    status: str


def normalize_secret_payload(payload: str) -> str:
    return payload.strip()


def parse_json_secret(payload: str) -> Dict[str, Any]:
    import json

    return json.loads(payload)


def validate_secret_labels(labels: Dict[str, str]) -> bool:
    if not labels:
        return False
    return all(isinstance(k, str) and isinstance(v, str) for k, v in labels.items())
