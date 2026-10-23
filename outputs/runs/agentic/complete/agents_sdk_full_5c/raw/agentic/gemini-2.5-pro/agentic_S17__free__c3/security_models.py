from dataclasses import dataclass
from typing import Optional, List

@dataclass
class EncryptionRequest:
    key_id: str
    plaintext: bytes

@dataclass
class EncryptionResponse:
    ciphertext: bytes
    key_id: str
    success: bool
    error: Optional[str] = None

@dataclass
class DecryptionRequest:
    ciphertext: bytes

@dataclass
class DecryptionResponse:
    plaintext: bytes
    key_id: str
    success: bool
    error: Optional[str] = None

@dataclass
class EnvelopeEncryptionRequest:
    key_id: str
    plaintext: bytes

@dataclass
class EnvelopeEncryptionResponse:
    ciphertext: bytes
    encrypted_data_key: bytes
    success: bool
    error: Optional[str] = None

@dataclass
class SigningRequest:
    key_id: str
    message: bytes

@dataclass
class SigningResponse:
    signature: bytes
    success: bool
    error: Optional[str] = None

@dataclass
class VerificationRequest:
    key_id: str
    message: bytes
    signature: bytes

@dataclass
class VerificationResponse:
    is_valid: bool
    success: bool
    error: Optional[str] = None

@dataclass
class AuditNote:
    timestamp: str
    event_name: str
    user: str
    details: str

@dataclass
class EmbeddingResponse:
    vectors: List[List[float]]
    success: bool
    error: Optional[str] = None

@dataclass
class SafetyCheckRequest:
    text: str

@dataclass
class SafetyCheckResponse:
    is_safe: bool
    scores: dict
    success: bool
    error: Optional[str] = None

@dataclass
class TranslationRequest:
    text: str
    target_language: str

@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language: str
    success: bool
    error: Optional[str] = None
