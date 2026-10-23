from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="ignore")
    return str(value)


@dataclass
class PayloadRequest:
    text: str
    key_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class CryptoResponse:
    key_id: Optional[str]
    ciphertext: Optional[str] = None
    plaintext: Optional[str] = None
    signature: Optional[str] = None
    verified: Optional[bool] = None
    summary: Optional[str] = None


def build_response(**kwargs: Any) -> CryptoResponse:
    return CryptoResponse(
        key_id=kwargs.get("key_id"),
        ciphertext=kwargs.get("ciphertext"),
        plaintext=kwargs.get("plaintext"),
        signature=kwargs.get("signature"),
        verified=kwargs.get("verified"),
        summary=kwargs.get("summary"),
    )
