from dataclasses import dataclass
from typing import Any, Dict, Optional


def _to_bytes(value: Any) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)
    return str(value).encode("utf-8")


def normalize_text(value: Any) -> str:
    return _to_bytes(value).decode("utf-8", errors="replace")


@dataclass
class PayloadRequest:
    plaintext: str
    key_id: str
    context: Optional[Dict[str, str]] = None


@dataclass
class PayloadResponse:
    key_id: str
    ciphertext: str
    plaintext: Optional[str] = None
    algorithm: Optional[str] = None


def normalize_context(context: Optional[Dict[str, Any]]) -> Dict[str, str]:
    return {str(k): normalize_text(v) for k, v in (context or {}).items()}
