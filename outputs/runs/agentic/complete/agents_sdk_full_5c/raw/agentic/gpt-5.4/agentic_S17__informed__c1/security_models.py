from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import base64
import json


@dataclass
class EncryptionRequest:
    key_id: str
    plaintext: str
    encryption_context: Optional[Dict[str, str]] = None

    def plaintext_bytes(self) -> bytes:
        return self.plaintext.encode("utf-8")


@dataclass
class EncryptionResponse:
    key_id: str
    ciphertext_b64: str
    provider: str = "aws-kms"
    algorithm: Optional[str] = None
    key_arn: Optional[str] = None


@dataclass
class DecryptionRequest:
    ciphertext_b64: str
    encryption_context: Optional[Dict[str, str]] = None

    def ciphertext_bytes(self) -> bytes:
        return base64.b64decode(self.ciphertext_b64)


@dataclass
class DecryptionResponse:
    plaintext: str
    key_id: Optional[str] = None
    provider: str = "aws-kms"
    encryption_algorithm: Optional[str] = None


@dataclass
class EnvelopeEncryptionResponse:
    key_id: str
    ciphertext_b64: str
    encrypted_data_key_b64: str
    iv_b64: str
    provider: str = "aws-kms"
    wrapping_algorithm: str = "SYMMETRIC_DEFAULT"
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class SignatureResponse:
    key_id: str
    message_type: str
    signing_algorithm: str
    signature_b64: str
    provider: str = "aws-kms"


@dataclass
class VerificationResponse:
    key_id: str
    signature_valid: bool
    signing_algorithm: str
    provider: str = "aws-kms"


@dataclass
class KeyUsageSummary:
    provider: str
    total_events: int
    operation_counts: Dict[str, int]
    recent_events: List[Dict[str, Any]]


@dataclass
class PayloadSafetyResult:
    provider: str
    safe: bool
    category_scores: Dict[str, float]
    blocked: bool
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
    translated_text: str
    target_language: str
    detected_source_language: Optional[str] = None


def b64encode_str(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")



def compact_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, separators=(",", ":"), sort_keys=True)
