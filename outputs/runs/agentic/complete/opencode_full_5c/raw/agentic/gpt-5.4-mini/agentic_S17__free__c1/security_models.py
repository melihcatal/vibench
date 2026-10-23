from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class CryptoRequest:
    key_id: str
    payload: str
    context: Optional[Dict[str, str]] = None


@dataclass
class CryptoResponse:
    key_id: str
    result: str
    metadata: Dict[str, Any]


def normalize_context(context: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not context:
        return {}
    return {str(k): str(v) for k, v in context.items()}


def normalize_payload(payload: Any) -> str:
    if payload is None:
        return ""
    return payload if isinstance(payload, str) else str(payload)
