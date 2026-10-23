from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import base64
import json


def _b64encode(value: bytes) -> str:
    return base64.b64encode(value).decode("utf-8")


def _b64decode(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))


@dataclass
class CryptoRequest:
    key_id: str
    plaintext: Optional[str] = None
    ciphertext: Optional[str] = None
    encryption_context: Dict[str, str] = field(default_factory=dict)
    signing_algorithm: Optional[str] = None
    message: Optional[str] = None
    message_type: str = "RAW"
    signature: Optional[str] = None

    def plaintext_bytes(self) -> bytes:
        return (self.plaintext or "").encode("utf-8")

    def message_bytes(self) -> bytes:
        return (self.message or "").encode("utf-8")


@dataclass
class CryptoResult:
    provider: str
    key_id: str
    algorithm: Optional[str] = None
    ciphertext: Optional[str] = None
    plaintext: Optional[str] = None
    plaintext_base64: Optional[str] = None
    signature: Optional[str] = None
    verified: Optional[bool] = None
    encryption_context: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "key_id": self.key_id,
            "algorithm": self.algorithm,
            "ciphertext": self.ciphertext,
            "plaintext": self.plaintext,
            "plaintext_base64": self.plaintext_base64,
            "signature": self.signature,
            "verified": self.verified,
            "encryption_context": self.encryption_context,
            "metadata": self.metadata,
        }


@dataclass
class EnvelopeEncryptRequest:
    key_id: str
    plaintext: str
    encryption_context: Dict[str, str] = field(default_factory=dict)
    data_key_spec: str = "AES_256"


@dataclass
class EnvelopeEncryptResult:
    provider: str
    key_id: str
    wrapped_data_key: str
    ciphertext: str
    nonce: str
    tag: str
    algorithm: str
    encryption_context: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "key_id": self.key_id,
            "wrapped_data_key": self.wrapped_data_key,
            "ciphertext": self.ciphertext,
            "nonce": self.nonce,
            "tag": self.tag,
            "algorithm": self.algorithm,
            "encryption_context": self.encryption_context,
        }


@dataclass
class KeyUsageSummary:
    provider: str
    key_id: str
    event_count: int
    operation_counts: Dict[str, int]
    principals: List[str]
    first_seen: Optional[str]
    last_seen: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "key_id": self.key_id,
            "event_count": self.event_count,
            "operation_counts": self.operation_counts,
            "principals": self.principals,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
        }


@dataclass
class SafetyAssessment:
    provider: str
    model: str
    safe: bool
    scores: Dict[str, float]
    flagged_categories: List[str]
    raw_response: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "safe": self.safe,
            "scores": self.scores,
            "flagged_categories": self.flagged_categories,
            "raw_response": self.raw_response,
        }


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    vector: List[float]
    dimensions: int
    input_text: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "vector": self.vector,
            "dimensions": self.dimensions,
            "input_text": self.input_text,
        }


@dataclass
class TranslationResult:
    provider: str
    source_language: str
    target_language: str
    translated_text: str
    detected_language: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "translated_text": self.translated_text,
            "detected_language": self.detected_language,
        }


def encode_bytes(value: bytes) -> str:
    return _b64encode(value)


def decode_bytes(value: str) -> bytes:
    return _b64decode(value)


def compact_json(value: Dict[str, Any]) -> str:
    return json.dumps(value, separators=(",", ":"), sort_keys=True)
