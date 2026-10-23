from dataclasses import dataclass
from typing import Optional, List, Any


@dataclass
class EncryptionRequest:
    key_id: str
    plaintext: bytes
    encryption_context: Optional[dict] = None


@dataclass
class EncryptionResponse:
    ciphertext: bytes
    key_id: str


@dataclass
class DecryptionRequest:
    key_id: str
    ciphertext: bytes
    encryption_context: Optional[dict] = None


@dataclass
class DecryptionResponse:
    plaintext: bytes
    key_id: str


@dataclass
class EnvelopeEncryptionRequest:
    key_id: str
    plaintext: bytes


@dataclass
class EnvelopeEncryptionResponse:
    ciphertext: bytes
    encrypted_data_key: bytes


@dataclass
class SigningRequest:
    key_id: str
    message: bytes
    signing_algorithm: str


@dataclass
class SigningResponse:
    signature: bytes
    key_id: str
    signing_algorithm: str


@dataclass
class VerificationRequest:
    key_id: str
    message: bytes
    signature: bytes
    signing_algorithm: str


@dataclass
class VerificationResponse:
    is_valid: bool
    key_id: str
    signing_algorithm: str


@dataclass
class KeyUsageSummaryRequest:
    events: List[str]


@dataclass
class KeyUsageSummaryResponse:
    summary: str


@dataclass
class PayloadSafetyRequest:
    payload: str


@dataclass
class PayloadSafetyResponse:
    is_safe: bool
    details: Optional[Any] = None


@dataclass
class CryptoAuditEmbeddingRequest:
    notes: List[str]


@dataclass
class CryptoAuditEmbeddingResponse:
    embeddings: List[List[float]]


@dataclass
class ComplianceNoteTranslateRequest:
    note: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class ComplianceNoteTranslateResponse:
    translated_note: str
    detected_source_language: Optional[str] = None
