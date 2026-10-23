from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import base64
import json


@dataclass
class EncryptionRequest:
    plaintext: str
    key_id: Optional[str] = None
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class EncryptionResponse:
    key_id: str
    ciphertext_b64: str
    provider: str = "aws-kms"
    algorithm: Optional[str] = None


@dataclass
class DecryptionRequest:
    ciphertext_b64: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class DecryptionResponse:
    key_id: str
    plaintext: str
    provider: str = "aws-kms"


@dataclass
class EnvelopeEncryptionResponse:
    key_id: str
    encrypted_data_key_b64: str
    nonce_b64: str
    ciphertext_b64: str
    provider: str = "aws-kms"
    wrapping_algorithm: str = "SYMMETRIC_DEFAULT"
    content_algorithm: str = "AESGCM"


@dataclass
class SignatureResponse:
    key_id: str
    message_type: str
    signing_algorithm: str
    signature_b64: str
    provider: str = "aws-kms"
    verified: Optional[bool] = None


@dataclass
class KeyUsageSummary:
    provider: str
    events_found: int
    keys: List[str]
    by_event_name: Dict[str, int]


@dataclass
class SafetyAssessment:
    provider: str
    flagged: bool
    categories: Dict[str, bool]
    original_text: str


@dataclass
class EmbeddingResponse:
    provider: str
    model: str
    vector: List[float]
    dimensions: int


@dataclass
class TranslationResponse:
    provider: str
    translated_text: str
    target_language: str
    source_language: Optional[str] = None


def b64encode_bytes(value: bytes) -> str:
    return base64.b64encode(value).decode("utf-8")


def b64decode_to_bytes(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))


def compact_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))
