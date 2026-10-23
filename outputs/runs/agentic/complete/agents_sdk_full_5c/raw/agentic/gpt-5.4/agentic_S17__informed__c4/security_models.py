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
    key_id: str
    plaintext: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class EnvelopeEncryptResponse:
    key_id: str
    encrypted_data_key_b64: str
    nonce_b64: str
    ciphertext_b64: str
    algorithm: str
    provider: str = "aws-kms"


@dataclass
class SignVerifyRequest:
    key_id: str
    message: str
    signature_b64: Optional[str] = None
    signing_algorithm: str = "RSASSA_PSS_SHA_256"
    verify: bool = False


@dataclass
class SignVerifyResponse:
    key_id: str
    operation: str
    signature_b64: Optional[str] = None
    verified: Optional[bool] = None
    algorithm: Optional[str] = None
    provider: str = "aws-kms"


@dataclass
class UsageSummary:
    provider: str
    window_start: Optional[str]
    window_end: Optional[str]
    event_count: int
    operations: Dict[str, int]
    notes: List[str] = field(default_factory=list)


@dataclass
class SafetyAssessment:
    provider: str
    flagged: bool
    categories: Dict[str, Any]
    raw: Dict[str, Any]


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    vector: List[float]
    dimensions: int


@dataclass
class TranslationResult:
    provider: str
    source_language: Optional[str]
    target_language: str
    translated_text: str


def text_to_bytes(value: str) -> bytes:
    return value.encode("utf-8")



def bytes_to_text(value: bytes) -> str:
    return value.decode("utf-8")



def b64encode_bytes(value: bytes) -> str:
    return base64.b64encode(value).decode("ascii")



def b64decode_text(value: str) -> bytes:
    return base64.b64decode(value.encode("ascii"))



def compact_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, separators=(",", ":"), sort_keys=True)
