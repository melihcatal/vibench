from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import base64


def b64encode_str(value: bytes) -> str:
    return base64.b64encode(value).decode("utf-8")


def b64decode_str(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))


def compact_dict(value: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in value.items() if v is not None}


@dataclass
class EncryptPayloadRequest:
    key_id: str
    plaintext: str
    encryption_context: Dict[str, str] = field(default_factory=dict)

    def plaintext_bytes(self) -> bytes:
        return self.plaintext.encode("utf-8")


@dataclass
class EncryptPayloadResponse:
    key_id: str
    ciphertext_b64: str
    provider: str
    algorithm: str
    encryption_context: Dict[str, str]

    def to_dict(self) -> Dict[str, Any]:
        return compact_dict(
            {
                "key_id": self.key_id,
                "ciphertext_b64": self.ciphertext_b64,
                "provider": self.provider,
                "algorithm": self.algorithm,
                "encryption_context": self.encryption_context,
            }
        )


@dataclass
class DecryptPayloadRequest:
    ciphertext_b64: str
    encryption_context: Dict[str, str] = field(default_factory=dict)

    def ciphertext_bytes(self) -> bytes:
        return b64decode_str(self.ciphertext_b64)


@dataclass
class DecryptPayloadResponse:
    plaintext: str
    key_id: Optional[str]
    provider: str
    algorithm: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return compact_dict(
            {
                "plaintext": self.plaintext,
                "key_id": self.key_id,
                "provider": self.provider,
                "algorithm": self.algorithm,
            }
        )


@dataclass
class EnvelopeEncryptRequest:
    key_id: str
    plaintext: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class EnvelopeEncryptResponse:
    provider: str
    key_id: str
    wrapped_data_key_b64: str
    ciphertext_b64: str
    nonce_b64: str
    encryption_context: Dict[str, str]

    def to_dict(self) -> Dict[str, Any]:
        return compact_dict(
            {
                "provider": self.provider,
                "key_id": self.key_id,
                "wrapped_data_key_b64": self.wrapped_data_key_b64,
                "ciphertext_b64": self.ciphertext_b64,
                "nonce_b64": self.nonce_b64,
                "encryption_context": self.encryption_context,
            }
        )


@dataclass
class SignOrVerifyRequest:
    key_id: str
    message: str
    action: str
    signature_b64: Optional[str] = None
    signing_algorithm: str = "RSASSA_PSS_SHA_256"
    message_type: str = "RAW"


@dataclass
class SignOrVerifyResponse:
    provider: str
    key_id: str
    action: str
    signature_b64: Optional[str] = None
    verified: Optional[bool] = None
    signing_algorithm: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return compact_dict(
            {
                "provider": self.provider,
                "key_id": self.key_id,
                "action": self.action,
                "signature_b64": self.signature_b64,
                "verified": self.verified,
                "signing_algorithm": self.signing_algorithm,
            }
        )


@dataclass
class KeyUsageSummaryRequest:
    events: List[Dict[str, Any]]


@dataclass
class KeyUsageSummaryResponse:
    provider: str
    model: str
    summary: str

    def to_dict(self) -> Dict[str, Any]:
        return {"provider": self.provider, "model": self.model, "summary": self.summary}


@dataclass
class PayloadSafetyRequest:
    text: str
    language: str = "en"


@dataclass
class PayloadSafetyResponse:
    provider: str
    blocked: bool
    scores: Dict[str, float]
    raw_result: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "blocked": self.blocked,
            "scores": self.scores,
            "raw_result": self.raw_result,
        }


@dataclass
class CryptoAuditEmbeddingRequest:
    notes: List[str]
    input_type: str = "search_document"


@dataclass
class CryptoAuditEmbeddingResponse:
    provider: str
    model: str
    embeddings: List[List[float]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "embeddings": self.embeddings,
        }


@dataclass
class ComplianceNoteTranslateRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class ComplianceNoteTranslateResponse:
    provider: str
    translated_text: str
    target_language: str
    detected_source_language: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return compact_dict(
            {
                "provider": self.provider,
                "translated_text": self.translated_text,
                "target_language": self.target_language,
                "detected_source_language": self.detected_source_language,
            }
        )
