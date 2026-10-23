from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PayloadRequest:
    payload: str
    aad: Optional[str] = None


@dataclass
class CiphertextResponse:
    ciphertext: str
    key_name: str


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def normalize_payload_request(data: Dict[str, Any]) -> PayloadRequest:
    return PayloadRequest(payload=normalize_text(data.get("payload")), aad=normalize_text(data.get("aad")) or None)
