from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_bytes(value: Any) -> bytes:
    if value is None:
        return b''
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode('utf-8')
    return str(value).encode('utf-8')


def normalize_text(value: Any) -> str:
    if value is None:
        return ''
    if isinstance(value, bytes):
        return value.decode('utf-8', errors='replace')
    return str(value)


@dataclass
class EncryptPayloadRequest:
    key_id: str
    plaintext: Any


@dataclass
class DecryptPayloadRequest:
    key_id: str
    ciphertext: Any


@dataclass
class EnvelopeEncryptRequest:
    key_id: str
    plaintext: Any


@dataclass
class SignOrVerifyRequest:
    key_id: str
    message: Any
    signature: Optional[Any] = None


@dataclass
class KeyUsageSummary:
    key_id: str
    event_count: int
    event_type: str


@dataclass
class PayloadSafetyResult:
    text: str
    is_safe: bool
    reasons: list


@dataclass
class CryptoAuditNote:
    note: str
    embedding: Optional[list] = None


@dataclass
class ComplianceNoteTranslation:
    source_text: str
    target_language: str
    translated_text: str


def response_map(**kwargs: Any) -> Dict[str, Any]:
    return dict(kwargs)
