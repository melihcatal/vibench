from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import base64
import json


def b64encode_str(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def b64decode_str(data: str) -> bytes:
    return base64.b64decode(data.encode("utf-8"))


@dataclass
class EncryptionRequest:
    key_id: str
    plaintext: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class EncryptionResponse:
    key_id: str
    ciphertext_b64: str


@dataclass
class DecryptionRequest:
    ciphertext_b64: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class DecryptionResponse:
    plaintext: str
    key_id: Optional[str] = None


@dataclass
class EnvelopeEncryptionResponse:
    key_id: str
    wrapped_data_key_b64: str
    nonce_b64: str
    ciphertext_b64: str


@dataclass
class SignatureRequest:
    key_id: str
    message: str
    algorithm: str = "RSASSA_PSS_SHA_256"


@dataclass
class VerificationRequest:
    key_id: str
    message: str
    signature_b64: str
    algorithm: str = "RSASSA_PSS_SHA_256"


@dataclass
class KeyUsageSummary:
    total_events: int
    by_method: Dict[str, int]
    affected_resources: List[str]


@dataclass
class SafetyCheckResult:
    is_safe: bool
    categories: List[str]
    provider: str = "OpenAI"


@dataclass
class EmbeddingResult:
    vector: List[float]
    provider: str = "OpenAI"
    model: str = "text-embedding-3-small"


@dataclass
class TranslationResult:
    translated_text: str
    provider: str = "Google Cloud Translation"
    target_language: str = "en"


def to_json(data: Any) -> str:
    if hasattr(data, "__dataclass_fields__"):
        return json.dumps(data.__dict__, ensure_ascii=False, sort_keys=True)
    return json.dumps(data, ensure_ascii=False, sort_keys=True)
