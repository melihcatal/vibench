from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import base64
import json


@dataclass
class EncryptRequest:
    plaintext: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class EncryptResponse:
    key_id: str
    ciphertext_b64: str
    provider: str = "aws-kms"


@dataclass
class DecryptRequest:
    ciphertext_b64: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class DecryptResponse:
    key_id: str
    plaintext: str
    provider: str = "aws-kms"


@dataclass
class EnvelopeEncryptRequest:
    plaintext: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class EnvelopeEncryptResponse:
    key_id: str
    ciphertext_b64: str
    encrypted_data_key_b64: str
    iv_b64: str
    algorithm: str
    provider: str = "aws-kms"


@dataclass
class SignatureRequest:
    message: str
    message_type: str = "RAW"
    signing_algorithm: str = "RSASSA_PSS_SHA_256"


@dataclass
class SignatureResponse:
    key_id: str
    signature_b64: str
    signing_algorithm: str
    provider: str = "aws-kms"


@dataclass
class VerificationResponse:
    key_id: str
    signature_valid: bool
    signing_algorithm: str
    provider: str = "aws-kms"


@dataclass
class KeyUsageSummary:
    key_id: str
    cloudtrail_events: List[Dict[str, Any]]
    counts_by_event: Dict[str, int]
    provider: str = "aws-cloudtrail"


@dataclass
class SafetyAssessment:
    text: str
    unsafe: bool
    categories: Dict[str, float]
    provider: str


@dataclass
class EmbeddingResponse:
    text: str
    embedding: List[float]
    dimensions: int
    provider: str
    model: str


@dataclass
class TranslationResponse:
    source_text: str
    translated_text: str
    target_language: str
    provider: str


def b64encode_bytes(value: bytes) -> str:
    return base64.b64encode(value).decode("utf-8")


def b64decode_text(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))


def compact_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, separators=(",", ":"), sort_keys=True)
