import dataclasses
from typing import Optional, Dict, Any


@dataclasses.dataclass
class EncryptRequest:
    plaintext: str
    key_name: str


@dataclasses.dataclass
class EncryptResponse:
    ciphertext: bytes
    key_name: str


@dataclasses.dataclass
class DecryptRequest:
    ciphertext: bytes
    key_name: str


@dataclasses.dataclass
class DecryptResponse:
    plaintext: str
    key_name: str


@dataclasses.dataclass
class EnvelopeEncryptRequest:
    plaintext: str
    key_name: str


@dataclasses.dataclass
class EnvelopeEncryptResponse:
    encrypted_dek: bytes
    encrypted_payload: bytes
    key_name: str


@dataclasses.dataclass
class SignRequest:
    message: str
    key_name: str


@dataclasses.dataclass
class SignResponse:
    signature: bytes
    key_name: str


@dataclasses.dataclass
class VerifyRequest:
    message: str
    signature: bytes
    key_name: str


@dataclasses.dataclass
class VerifyResponse:
    is_valid: bool
    key_name: str


@dataclasses.dataclass
class KeyUsageSummaryRequest:
    usage_logs: str


@dataclasses.dataclass
class KeyUsageSummaryResponse:
    summary: str


@dataclasses.dataclass
class PayloadSafetyRequest:
    payload_text: str


@dataclasses.dataclass
class PayloadSafetyResponse:
    unsafe_score: float
    is_safe: bool


@dataclasses.dataclass
class CryptoAuditEmbeddingRequest:
    audit_notes: str


@dataclasses.dataclass
class CryptoAuditEmbeddingResponse:
    embedding_vector: list[float]


@dataclasses.dataclass
class ComplianceNoteTranslateRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclasses.dataclass
class ComplianceNoteTranslateResponse:
    translated_text: str
    source_language: str
    target_language: str
