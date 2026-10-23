from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import base64


def b64encode_str(value: bytes) -> str:
    return base64.b64encode(value).decode("utf-8")


def b64decode_bytes(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))


def normalize_text(value: str) -> str:
    return " ".join(value.strip().split())


def compact_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for key, val in (metadata or {}).items():
        if val is None:
            continue
        result[str(key)] = str(val)
    return result


@dataclass
class EncryptRequest:
    plaintext: str
    key_id: str
    context: Dict[str, str] = field(default_factory=dict)


@dataclass
class EncryptResponse:
    key_id: str
    ciphertext: str
    provider: str
    algorithm: str


@dataclass
class DecryptRequest:
    ciphertext: str
    key_id: Optional[str] = None
    context: Dict[str, str] = field(default_factory=dict)


@dataclass
class DecryptResponse:
    key_id: str
    plaintext: str
    provider: str


@dataclass
class EnvelopeEncryptRequest:
    plaintext: str
    key_id: str
    context: Dict[str, str] = field(default_factory=dict)


@dataclass
class EnvelopeEncryptResponse:
    key_id: str
    encrypted_payload: str
    encrypted_data_key: str
    provider: str
    wrapping_algorithm: str


@dataclass
class SignatureRequest:
    message: str
    key_id: str
    action: str
    signature: Optional[str] = None
    signing_algorithm: str = "RSASSA_PSS_SHA_256"


@dataclass
class SignatureResponse:
    key_id: str
    provider: str
    action: str
    signature: Optional[str] = None
    verified: Optional[bool] = None


@dataclass
class UsageSummary:
    provider: str
    key_id: str
    total_events: int
    event_types: Dict[str, int]
    recent_events: List[Dict[str, Any]]


@dataclass
class SafetyCheckResult:
    provider: str
    safe: bool
    categories: Dict[str, bool]
    model: str


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
