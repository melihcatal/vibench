import dataclasses
from typing import Dict, Any, Optional

@dataclasses.dataclass
class EncryptionRequest:
    plaintext: bytes
    project_id: str
    location: str
    key_ring: str
    key_id: str

@dataclasses.dataclass
class EncryptionResponse:
    ciphertext: bytes

@dataclasses.dataclass
class DecryptionRequest:
    ciphertext: bytes
    project_id: str
    location: str
    key_ring: str
    key_id: str

@dataclasses.dataclass
class DecryptionResponse:
    plaintext: bytes

@dataclasses.dataclass
class EnvelopeEncryptionRequest:
    plaintext: bytes
    project_id: str
    location: str
    key_ring: str
    key_id: str

@dataclasses.dataclass
class EnvelopeEncryptionResponse:
    encrypted_data: bytes
    encrypted_data_key: bytes

@dataclasses.dataclass
class EnvelopeDecryptionRequest:
    encrypted_data: bytes
    encrypted_data_key: bytes
    project_id: str
    location: str
    key_ring: str
    key_id: str

@dataclasses.dataclass
class EnvelopeDecryptionResponse:
    plaintext: bytes

@dataclasses.dataclass
class SignRequest:
    message: bytes
    project_id: str
    location: str
    key_ring: str
    key_id: str
    version_id: str

@dataclasses.dataclass
class SignResponse:
    signature: bytes

@dataclasses.dataclass
class VerifyRequest:
    message: bytes
    signature: bytes
    project_id: str
    location: str
    key_ring: str
    key_id: str
    version_id: str

@dataclasses.dataclass
class VerifyResponse:
    is_valid: bool

@dataclasses.dataclass
class KeyUsageSummaryRequest:
    project_id: str
    time_window_seconds: int = 3600 # Last hour by default

@dataclasses.dataclass
class KeyUsageSummaryResponse:
    summary: Dict[str, Any]

@dataclasses.dataclass
class PayloadSafetyRequest:
    text_payload: str
    project_id: str

@dataclasses.dataclass
class PayloadSafetyResponse:
    is_safe: bool
    moderation_results: Dict[str, Any]

@dataclasses.dataclass
class CryptoAuditEmbeddingRequest:
    audit_notes: str
    project_id: str
    location: str

@dataclasses.dataclass
class CryptoAuditEmbeddingResponse:
    embedding: list[float]

@dataclasses.dataclass
class ComplianceNoteTranslateRequest:
    text: str
    target_language_code: str
    project_id: str
    location: str

@dataclasses.dataclass
class ComplianceNoteTranslateResponse:
    translated_text: str
    source_language_code: str
