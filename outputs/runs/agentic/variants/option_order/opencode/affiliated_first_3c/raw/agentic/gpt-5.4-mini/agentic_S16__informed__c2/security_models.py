from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SecretRequest:
    name: str
    version_stage: Optional[str] = None


@dataclass
class SecretResponse:
    name: str
    value: Any
    version_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


def normalize_secret_value(value: Any) -> Any:
    if isinstance(value, bytes):
        return value.decode()
    return value


def normalize_text(text: Any) -> str:
    if text is None:
        return ""
    return str(text).strip()
