from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import base64
import json


def ensure_bytes(value: str | bytes) -> bytes:
    if isinstance(value, bytes):
        return value
    return value.encode("utf-8")


def b64encode_str(value: bytes) -> str:
    return base64.b64encode(value).decode("ascii")


def b64decode_str(value: str) -> bytes:
    return base64.b64decode(value.encode("ascii"))


def compact_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, separators=(",", ":"), sort_keys=True)


@dataclass
class EncryptionRequest:
    plaintext: str
    key_id: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class EncryptionResponse:
    key_id: str
    ciphertext_b64: str
    provider: str = "aws-kms"


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
    ciphertext_b64: str
    iv_b64: str
    tag_b64: str
    provider: str = "aws-kms"


@dataclass
class SignVerifyRequest:
    key_id: str
    message: str
    signature_b64: Optional[str] = None
    signing_algorithm: str = "RSASSA_PSS_SHA_256"


@dataclass
class KeyUsageSummary:
    key_id: str
    total_events: int
    actions: Dict[str, int]
    recent_events: List[Dict[str, Any]]
    provider: str = "aws-cloudtrail"


@dataclass
class SafetyResult:
    model: str
    safe: bool
    categories: Dict[str, Any]
    provider: str = "openai"


@dataclass
class EmbeddingResult:
    model: str
    vector: List[float]
    provider: str = "openai"


@dataclass
class TranslationResult:
    model: str
    translated_text: str
    provider: str = "openai"
