from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class EncryptionRequest:
    key_id: str
    plaintext: bytes
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class EncryptionResponse:
    ciphertext: bytes
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class DecryptionRequest:
    ciphertext: bytes
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class DecryptionResponse:
    plaintext: bytes
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class EnvelopeEncryptionRequest:
    key_id: str
    plaintext: bytes
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class EnvelopeEncryptionResponse:
    ciphertext_blob: bytes
    key_id: str
    plaintext_data_key: bytes
    ciphertext_data_key: bytes
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class SigningRequest:
    key_id: str
    message: bytes
    signing_algorithm: str
    message_type: str = "DIGEST"


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
    message_type: str = "DIGEST"


@dataclass
class VerificationResponse:
    signature_valid: bool
    key_id: str
    signing_algorithm: str


@dataclass
class KeyUsageEvent:
    event_id: str
    key_id: str
    event_type: str
    timestamp: str
    details: Dict[str, Any]


@dataclass
class PayloadScanRequest:
    payload_text: str


@dataclass
class PayloadScanResponse:
    is_safe: bool
    findings: Optional[Dict[str, Any]] = None


@dataclass
class AuditNote:
    note_id: str
    content: str
    timestamp: str
    key_id: Optional[str] = None
    related_event_id: Optional[str] = None


@dataclass
class AuditNoteEmbedding:
    note_id: str
    embedding: list[float]


@dataclass
class TranslationRequest:
    text: str
    source_language: Optional[str] = None
    target_language: str


@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str
