from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SecurityRequest:
    payload: str
    key_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


@dataclass
class SecurityResponse:
    provider: str
    result: Any
    metadata: Dict[str, Any]


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value).strip()


def normalize_mapping(value: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return dict(value or {})
