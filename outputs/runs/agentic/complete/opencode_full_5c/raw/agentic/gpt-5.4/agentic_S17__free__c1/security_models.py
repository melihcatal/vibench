from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import base64
import json


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def to_bytes(value: str | bytes) -> bytes:
    if isinstance(value, bytes):
        return value
    return value.encode("utf-8")


def b64encode_str(value: bytes) -> str:
    return base64.b64encode(value).decode("ascii")


def b64decode_str(value: str) -> bytes:
    return base64.b64decode(value.encode("ascii"))


def normalize_metadata(metadata: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    normalized: Dict[str, str] = {}
    for key, value in (metadata or {}).items():
        normalized[str(key)] = (
            json.dumps(value, sort_keys=True)
            if isinstance(value, (dict, list))
            else str(value)
        )
    return normalized


@dataclass
class PayloadRequest:
    key_id: str
    plaintext: str
    encryption_context: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, str] = field(default_factory=dict)

    def plaintext_bytes(self) -> bytes:
        return to_bytes(self.plaintext)


@dataclass
class CiphertextResponse:
    key_id: str
    provider: str
    ciphertext_b64: str
    algorithm: str
    encryption_context: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_id": self.key_id,
            "provider": self.provider,
            "ciphertext_b64": self.ciphertext_b64,
            "algorithm": self.algorithm,
            "encryption_context": self.encryption_context,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }


@dataclass
class PlaintextResponse:
    key_id: str
    provider: str
    plaintext: str
    encryption_context: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, str] = field(default_factory=dict)
    decrypted_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_id": self.key_id,
            "provider": self.provider,
            "plaintext": self.plaintext,
            "encryption_context": self.encryption_context,
            "metadata": self.metadata,
            "decrypted_at": self.decrypted_at,
        }


@dataclass
class EnvelopeEncryptionResponse:
    provider: str
    kms_key_id: str
    encrypted_data_key_b64: str
    ciphertext_b64: str
    nonce_b64: str
    algorithm: str
    wrapping_algorithm: str
    encryption_context: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "kms_key_id": self.kms_key_id,
            "encrypted_data_key_b64": self.encrypted_data_key_b64,
            "ciphertext_b64": self.ciphertext_b64,
            "nonce_b64": self.nonce_b64,
            "algorithm": self.algorithm,
            "wrapping_algorithm": self.wrapping_algorithm,
            "encryption_context": self.encryption_context,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }


@dataclass
class SignatureResponse:
    provider: str
    key_id: str
    algorithm: str
    action: str
    signature_b64: Optional[str] = None
    verified: Optional[bool] = None
    message_type: str = "RAW"
    created_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "key_id": self.key_id,
            "algorithm": self.algorithm,
            "action": self.action,
            "signature_b64": self.signature_b64,
            "verified": self.verified,
            "message_type": self.message_type,
            "created_at": self.created_at,
        }


@dataclass
class KeyUsageEvent:
    provider: str
    event_type: str
    key_id: str
    timestamp: str
    status: str
    region: Optional[str] = None
    actor: Optional[str] = None
    source: Optional[str] = None


@dataclass
class SafetyCheckResult:
    provider: str
    model: str
    is_safe: bool
    categories: List[str]
    details: Dict[str, Any]
    checked_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "is_safe": self.is_safe,
            "categories": self.categories,
            "details": self.details,
            "checked_at": self.checked_at,
        }


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    vector: List[float]
    dimensions: int
    created_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "vector": self.vector,
            "dimensions": self.dimensions,
            "created_at": self.created_at,
        }


@dataclass
class TranslationResult:
    provider: str
    source_language: str
    target_language: str
    translated_text: str
    created_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "translated_text": self.translated_text,
            "created_at": self.created_at,
        }
