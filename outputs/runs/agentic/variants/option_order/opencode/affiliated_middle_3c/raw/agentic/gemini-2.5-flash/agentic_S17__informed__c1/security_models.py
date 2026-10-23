import dataclasses
from typing import Optional, Dict, Any


@dataclasses.dataclass
class EncryptionRequest:
    key_name: str
    plaintext: str


@dataclasses.dataclass
class EncryptionResponse:
    ciphertext: str
    key_name: str


@dataclasses.dataclass
class DecryptionRequest:
    key_name: str
    ciphertext: str


@dataclasses.dataclass
class DecryptionResponse:
    plaintext: str
    key_name: str


@dataclasses.dataclass
class EnvelopeEncryptionRequest:
    key_name: str
    plaintext: str


@dataclasses.dataclass
class EnvelopeEncryptionResponse:
    encrypted_data_key: str
    ciphertext: str
    key_name: str


@dataclasses.dataclass
class SignRequest:
    key_name: str
    message: str


@dataclasses.dataclass
class SignResponse:
    signature: str
    key_name: str


@dataclasses.dataclass
class VerifyRequest:
    key_name: str
    message: str
    signature: str


@dataclasses.dataclass
class VerifyResponse:
    is_valid: bool
    key_name: str


@dataclasses.dataclass
class KeyUsageSummaryRequest:
    audit_logs: str


@dataclasses.dataclass
class KeyUsageSummaryResponse:
    summary: str


@dataclasses.dataclass
class PayloadSafetyRequest:
    decrypted_payload: str


@dataclasses.dataclass
class PayloadSafetyResponse:
    is_safe: bool
    scores: Dict[str, Any]


@dataclasses.dataclass
class CryptoAuditEmbeddingRequest:
    audit_note: str


@dataclasses.dataclass
class CryptoAuditEmbeddingResponse:
    embedding: list[float]


@dataclasses.dataclass
class ComplianceNoteTranslateRequest:
    note_text: str
    target_language: str


@dataclasses.dataclass
class ComplianceNoteTranslateResponse:
    translated_text: str
    source_language: str
    target_language: str
