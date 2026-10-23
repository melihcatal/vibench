from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class EncryptRequest:
    key_id: str
    plaintext: str


@dataclass
class EncryptResponse:
    ciphertext_blob: str
    key_id: str


@dataclass
class DecryptRequest:
    ciphertext_blob: str


@dataclass
class DecryptResponse:
    plaintext: str
    key_id: str


@dataclass
class EnvelopeEncryptRequest:
    key_id: str
    plaintext: str


@dataclass
class EnvelopeEncryptResponse:
    encrypted_data_key: str
    ciphertext_blob: str


@dataclass
class SignRequest:
    key_id: str
    message: str
    signing_algorithm: str


@dataclass
class SignResponse:
    signature: str
    key_id: str
    signing_algorithm: str


@dataclass
class VerifyRequest:
    key_id: str
    message: str
    signature: str
    signing_algorithm: str


@dataclass
class VerifyResponse:
    signature_valid: bool
    key_id: str


@dataclass
class KeyUsageSummaryRequest:
    pass


@dataclass
class KeyUsageSummaryResponse:
    key_ids: List[str]
    summary_data: Dict[str, Any]


@dataclass
class PayloadSafetyRequest:
    text: str


@dataclass
class PayloadSafetyResponse:
    is_safe: bool
    details: Dict[str, Any]


@dataclass
class CryptoAuditEmbeddingRequest:
    notes: str


@dataclass
class CryptoAuditEmbeddingResponse:
    embedding: List[float]


@dataclass
class ComplianceNoteTranslateRequest:
    text: str
    source_language_code: str
    target_language_code: str


@dataclass
class ComplianceNoteTranslateResponse:
    translated_text: str
    source_language_code: str
    target_language_code: str
