from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import base64
import hashlib
import json


def _json_default(value: Any) -> Any:
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("utf-8")
    raise TypeError(f"Unsupported type: {type(value)!r}")


def normalize_plaintext(payload: Any) -> bytes:
    if isinstance(payload, bytes):
        return payload
    if isinstance(payload, str):
        return payload.encode("utf-8")
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), default=_json_default
    ).encode("utf-8")


def b64encode_bytes(value: bytes) -> str:
    return base64.b64encode(value).decode("utf-8")


def b64decode_text(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))


def sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


@dataclass
class EncryptRequest:
    plaintext: Any
    encryption_context: Dict[str, str] = field(default_factory=dict)
    key_id: Optional[str] = None


@dataclass
class EncryptResponse:
    key_id: str
    algorithm: str
    ciphertext: str
    plaintext_sha256: str
    provider: str


@dataclass
class DecryptRequest:
    ciphertext: str
    encryption_context: Dict[str, str] = field(default_factory=dict)
    key_id: Optional[str] = None


@dataclass
class DecryptResponse:
    key_id: str
    algorithm: str
    plaintext: str
    plaintext_sha256: str
    provider: str


@dataclass
class EnvelopeEncryptRequest:
    plaintext: Any
    encryption_context: Dict[str, str] = field(default_factory=dict)
    aad: Optional[str] = None
    key_id: Optional[str] = None


@dataclass
class EnvelopeEncryptResponse:
    key_id: str
    kms_provider: str
    wrapping_algorithm: str
    data_key_ciphertext: str
    ciphertext: str
    nonce: str
    tag: str
    plaintext_sha256: str


@dataclass
class SignVerifyRequest:
    message: Any
    operation: str
    signing_algorithm: str = "RSASSA_PSS_SHA_256"
    signature: Optional[str] = None
    key_id: Optional[str] = None


@dataclass
class SignVerifyResponse:
    key_id: str
    provider: str
    signing_algorithm: str
    message_sha256: str
    signature: Optional[str] = None
    valid: Optional[bool] = None


@dataclass
class KeyUsageSummary:
    provider: str
    key_id: Optional[str]
    event_count: int
    operations: List[str]
    summary: str


@dataclass
class PayloadSafetyResult:
    provider: str
    safe: bool
    scores: Dict[str, float]
    flagged_categories: List[str]


@dataclass
class AuditEmbeddingResult:
    provider: str
    model: str
    dimensions: int
    embedding: List[float]


@dataclass
class TranslationResult:
    provider: str
    target_language: str
    detected_source_language: Optional[str]
    translated_text: str
