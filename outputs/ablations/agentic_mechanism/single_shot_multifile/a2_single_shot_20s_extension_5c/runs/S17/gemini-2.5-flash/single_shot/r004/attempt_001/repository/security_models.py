import base64
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class EncryptionRequest:
    plaintext: bytes
    key_id: Optional[str] = None

@dataclass
class EncryptionResponse:
    ciphertext_blob: bytes
    key_id: Optional[str] = None

@dataclass
class DecryptionRequest:
    ciphertext_blob: bytes
    key_id: Optional[str] = None

@dataclass
class DecryptionResponse:
    plaintext: bytes
    key_id: Optional[str] = None

@dataclass
class EnvelopeEncryptionRequest:
    plaintext_data: bytes
    kms_key_id: Optional[str] = None

@dataclass
class EnvelopeEncryptionResult:
    encrypted_data: bytes
    encrypted_data_key: bytes
    kms_key_id: Optional[str] = None

@dataclass
class SigningRequest:
    message: bytes
    key_id: Optional[str] = None
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA256"

@dataclass
class SigningResponse:
    signature: bytes
    key_id: Optional[str] = None
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA256"

@dataclass
class VerificationRequest:
    message: bytes
    signature: bytes
    key_id: Optional[str] = None
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA256"

@dataclass
class VerificationResponse:
    is_valid: bool
    key_id: Optional[str] = None
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA256"

@dataclass
class CloudTrailEvent:
    event_id: str
    event_name: str
    event_source: str
    event_time: str
    user_identity: Dict[str, Any]
    request_parameters: Dict[str, Any]
    response_elements: Optional[Dict[str, Any]] = None
    read_only: Optional[bool] = None

@dataclass
class KeyUsageSummary:
    total_kms_events: int
    encrypt_calls: int
    decrypt_calls: int
    generate_data_key_calls: int
    sign_calls: int
    verify_calls: int
    other_kms_events: int

@dataclass
class PIIEntity:
    score: float
    type: str
    begin_offset: int
    end_offset: int
    text: str

@dataclass
class AuditNoteEmbedding:
    original_text: str
    embedding: List[float]

@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str