from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PayloadRequest:
    plaintext: str
    key_id: str
    aad: Optional[str] = None


@dataclass
class CiphertextResponse:
    ciphertext: str
    key_id: str
    metadata: Dict[str, Any]


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def normalize_mapping(data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return dict(data or {})
