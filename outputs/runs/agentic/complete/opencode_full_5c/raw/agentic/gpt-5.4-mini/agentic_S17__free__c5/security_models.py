from dataclasses import dataclass
from typing import Any, Dict, Optional


def _to_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def normalize_payload(value: Any) -> str:
    return _to_text(value).strip()


def normalize_dict(data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return dict(data or {})


@dataclass
class CryptoRequest:
    key_id: str
    payload: str
    context: Optional[Dict[str, Any]] = None


@dataclass
class CryptoResponse:
    key_id: str
    payload: str
    algorithm: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class EnvelopeRequest:
    key_id: str
    plaintext: str
    aad: Optional[Dict[str, Any]] = None


@dataclass
class VerificationRequest:
    key_id: str
    message: str
    signature: Optional[str] = None
    public_key_pem: Optional[str] = None
