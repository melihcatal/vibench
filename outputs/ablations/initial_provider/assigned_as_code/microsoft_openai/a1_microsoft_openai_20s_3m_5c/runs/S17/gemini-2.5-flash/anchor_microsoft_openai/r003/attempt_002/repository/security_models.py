from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class EncryptionRequest:
    plaintext: bytes
    key_id: str
    algorithm: Optional[str] = None

@dataclass
class EncryptionResponse:
    ciphertext: bytes
    iv: Optional[bytes] = None
    tag: Optional[bytes] = None
    key_id: str
    algorithm: str

@dataclass
class DecryptionRequest:
    ciphertext: bytes
    key_id: str
    iv: Optional[bytes] = None
    tag: Optional[bytes] = None
    algorithm: Optional[str] = None

@dataclass
class DecryptionResponse:
    plaintext: bytes
    key_id: str
    algorithm: str

@dataclass
class SignRequest:
    digest: bytes
    key_id: str
    algorithm: Optional[str] = None

@dataclass
class SignResponse:
    signature: bytes
    key_id: str
    algorithm: str

@dataclass
class VerifyRequest:
    digest: bytes
    signature: bytes
    key_id: str
    algorithm: Optional[str] = None

@dataclass
class VerifyResponse:
    is_valid: bool
    key_id: str
    algorithm: str

@dataclass
class EnvelopeEncryptionRequest:
    plaintext: bytes
    key_id: str
    algorithm: Optional[str] = None

@dataclass
class EnvelopeEncryptionResponse:
    ciphertext: bytes
    encrypted_key: bytes
    iv: Optional[bytes] = None
    tag: Optional[bytes] = None
    key_id: str
    algorithm: str

@dataclass
class KeyUsageSummaryRequest:
    project_id: str
    location: str
    key_ring_id: str
    crypto_key_id: str
    time_range: Optional[str] = None

@dataclass
class KeyUsageSummaryResponse:
    summary: Dict[str, Any]

@dataclass
class PayloadSafetyRequest:
    text_content: str
    project_id: str

@dataclass
class PayloadSafetyResponse:
    has_sensitive_data: bool
    findings: Any

@dataclass
class CryptoAuditEmbeddingRequest:
    audit_notes: str
    project_id: str
    location: str
    model_id: str

@dataclass
class CryptoAuditEmbeddingResponse:
    embedding: Any

@dataclass
class ComplianceNoteTranslateRequest:
    text: str
    target_language: str
    project_id: str
    location: str
    source_language: Optional[str] = None

@dataclass
class ComplianceNoteTranslateResponse:
    translated_text: str
    detected_source_language: Optional[str] = None
