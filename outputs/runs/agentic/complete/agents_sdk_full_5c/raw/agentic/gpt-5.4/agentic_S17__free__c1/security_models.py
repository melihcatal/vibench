from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import base64
import json


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def b64encode_str(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def b64decode_str(data: str) -> bytes:
    return base64.b64decode(data.encode("ascii"))


def json_dumps_canonical(value: Dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


@dataclass
class EncryptRequest:
    key_id: str
    plaintext: str
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class EncryptResponse:
    key_id: str
    ciphertext_b64: str
    provider: str
    algorithm: str


@dataclass
class DecryptRequest:
    ciphertext_b64: str
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class DecryptResponse:
    key_id: str
    plaintext: str
    provider: str


@dataclass
class EnvelopeEncryptRequest:
    key_id: str
    plaintext: str
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class EnvelopeEncryptResponse:
    key_id: str
    encrypted_data_key_b64: str
    nonce_b64: str
    ciphertext_b64: str
    provider: str
    wrapping_algorithm: str
    content_algorithm: str


@dataclass
class SignatureRequest:
    key_id: str
    message: str
    action: str
    signature_b64: Optional[str] = None
    message_type: str = "RAW"


@dataclass
class SignatureResponse:
    key_id: str
    action: str
    provider: str
    algorithm: str
    signature_b64: Optional[str] = None
    verified: Optional[bool] = None


@dataclass
class KeyUsageSummary:
    provider: str
    events: List[Dict[str, Any]]
    generated_at: str


@dataclass
class PayloadSafetyResult:
    provider: str
    safe: bool
    categories: Dict[str, Any]
    action: str


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
