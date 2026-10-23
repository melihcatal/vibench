from dataclasses import dataclass
from typing import Any, Mapping, Optional


def normalize_secret_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode()
    if isinstance(value, str):
        return value
    return str(value)


def extract_secret_payload(payload: Any) -> Any:
    if isinstance(payload, Mapping):
        for key in ("SecretString", "secretString", "value", "secret", "data"):
            if key in payload:
                return payload[key]
    return payload


@dataclass
class SecretRequest:
    name: str
    version_id: Optional[str] = None
    stage: Optional[str] = None


@dataclass
class SecretResponse:
    name: str
    value: str
    version_id: Optional[str] = None
