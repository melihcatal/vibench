from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class SecretRequest:
    secret_id: str
    version_id: Optional[str] = None


@dataclass
class SecretResponse:
    secret_value: str
    version_id: str
    metadata: Dict[str, Any]


@dataclass
class SecretVersion:
    version_id: str
    state: str
    created_at: str


def normalize_secret_value(secret_value: str) -> str:
    return secret_value.strip()
