from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import base64


def b64e(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def b64d(data: str) -> bytes:
    return base64.b64decode(data.encode("utf-8"))


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


@dataclass
class CryptoRequest:
    key_id: str
    plaintext: Optional[str] = None
    ciphertext: Optional[str] = None
    signing_algorithm: Optional[str] = None
    message: Optional[str] = None
    algorithm: Optional[str] = None
    context: Dict[str, str] = field(default_factory=dict)


@dataclass
class CryptoResponse:
    key_id: str
    algorithm: Optional[str] = None
    plaintext: Optional[str] = None
    ciphertext: Optional[str] = None
    signature: Optional[str] = None
    wrapped_key: Optional[str] = None
    iv: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_context(context: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not context:
        return {}
    return {str(k): normalize_text(v) for k, v in context.items()}
