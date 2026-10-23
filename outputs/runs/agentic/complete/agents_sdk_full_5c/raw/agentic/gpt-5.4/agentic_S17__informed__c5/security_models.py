from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import base64
import json


@dataclass
class CryptoRequest:
    key_id: str
    plaintext: Optional[str] = None
    plaintext_bytes: Optional[bytes] = None
    ciphertext_b64: Optional[str] = None
    algorithm: Optional[str] = None
    encryption_context: Dict[str, str] = field(default_factory=dict)

    def plaintext_as_bytes(self) -> bytes:
        if self.plaintext_bytes is not None:
            return self.plaintext_bytes
        if self.plaintext is None:
            raise ValueError("plaintext or plaintext_bytes is required")
        return self.plaintext.encode("utf-8")

    def ciphertext_bytes(self) -> bytes:
        if not self.ciphertext_b64:
            raise ValueError("ciphertext_b64 is required")
        return base64.b64decode(self.ciphertext_b64)


@dataclass
class CryptoResponse:
    provider: str
    key_id: str
    algorithm: Optional[str]
    ciphertext_b64: Optional[str] = None
    plaintext: Optional[str] = None
    plaintext_b64: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "key_id": self.key_id,
            "algorithm": self.algorithm,
            "ciphertext_b64": self.ciphertext_b64,
            "plaintext": self.plaintext,
            "plaintext_b64": self.plaintext_b64,
            "metadata": self.metadata,
        }


@dataclass
class EnvelopeEncryptionResponse:
    provider: str
    key_id: str
    kms_ciphertext_b64: str
    encrypted_data_key_b64: str
    nonce_b64: str
    ciphertext_b64: str
    algorithm: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "key_id": self.key_id,
            "kms_ciphertext_b64": self.kms_ciphertext_b64,
            "encrypted_data_key_b64": self.encrypted_data_key_b64,
            "nonce_b64": self.nonce_b64,
            "ciphertext_b64": self.ciphertext_b64,
            "algorithm": self.algorithm,
            "metadata": self.metadata,
        }


@dataclass
class KeyUsageSummary:
    provider: str
    model: str
    summary: str
    highlights: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "summary": self.summary,
            "highlights": self.highlights,
        }


@dataclass
class SafetyAssessment:
    provider: str
    verdict: str
    scores: Dict[str, Any]
    flagged: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "verdict": self.verdict,
            "scores": self.scores,
            "flagged": self.flagged,
        }


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    vector: List[float]
    dimensions: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "vector": self.vector,
            "dimensions": self.dimensions,
        }


@dataclass
class TranslationResult:
    provider: str
    translated_text: str
    target_language: str
    detected_source_language: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "translated_text": self.translated_text,
            "target_language": self.target_language,
            "detected_source_language": self.detected_source_language,
        }


def b64encode_str(value: bytes) -> str:
    return base64.b64encode(value).decode("ascii")


def compact_json(data: Any) -> str:
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False)
