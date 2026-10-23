from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SecretRequest:
    provider: str
    secret_id: str
    version: Optional[str] = None
    project_id: Optional[str] = None
    region: Optional[str] = None


@dataclass
class SecretResponse:
    provider: str
    secret_id: str
    value: str
    version: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


def normalize_secret_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return str(value)
