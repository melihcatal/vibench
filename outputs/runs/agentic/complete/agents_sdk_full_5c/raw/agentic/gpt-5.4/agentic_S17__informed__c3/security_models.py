from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import base64
import json


@dataclass
class EncryptRequest:
    key_id: str
    plaintext: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class EncryptResponse:
    key_id: str
    ciphertext_b64: str
    algorithm: str
    provider: str = "aws-kms"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DecryptRequest:
    ciphertext_b64: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class DecryptResponse:
    key_id: Optional[str]
    plaintext: str
    provider: str = "aws-kms"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EnvelopeEncryptRequest:
    key_id: str
    plaintext: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class EnvelopeEncryptResponse:
    key_id: str
    encrypted_data_key_b64: str
    ciphertext_b64: str
    iv_b64: str
    tag_b64: str
    wrapping_algorithm: str
    content_algorithm: str
    provider: str = "aws-kms"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SignatureResponse:
    key_id: str
    action: str
    algorithm: str
    provider: str = "aws-kms"
    signature_b64: Optional[str] = None
    verified: Optional[bool] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UsageSummary:
    key_id: Optional[str]
    event_count: int
    actions: Dict[str, int]
    provider: str = "aws-cloudtrail"
    source: str = "cloudtrail"


@dataclass
class SafetyCheckResult:
    provider: str
    model: str
    unsafe: bool
    scores: Dict[str, float]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    dimensions: int
    vector: List[float]


@dataclass
class TranslationResult:
    provider: str
    target_language: str
    translated_text: str
    detected_source_language: Optional[str] = None


def b64encode_bytes(value: bytes) -> str:
    return base64.b64encode(value).decode("utf-8")



def b64decode_text(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))



def normalize_text_payload(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload
    if isinstance(payload, bytes):
        return payload.decode("utf-8")
    return json.dumps(payload, sort_keys=True, ensure_ascii=False)
