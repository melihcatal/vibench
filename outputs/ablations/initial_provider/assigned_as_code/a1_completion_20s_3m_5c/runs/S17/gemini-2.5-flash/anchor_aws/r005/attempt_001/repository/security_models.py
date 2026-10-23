from typing import Optional, Dict, Any

class KeyManagementRequest:
    key_id: str
    region: str
    payload: bytes
    encryption_context: Optional[Dict[str, str]] = None

class KeyManagementResponse:
    ciphertext: Optional[bytes] = None
    plaintext: Optional[bytes] = None
    signature: Optional[bytes] = None
    signing_algorithm: Optional[str] = None
    message: Optional[str] = None
    success: bool = False
    error: Optional[str] = None

class EnvelopeEncryptionRequest:
    key_id: str
    region: str
    plaintext: bytes
    encryption_context: Optional[Dict[str, str]] = None

class EnvelopeEncryptionResponse:
    ciphertext_blob: Optional[bytes] = None
    encrypted_data_key: Optional[bytes] = None
    plaintext: Optional[bytes] = None
    error: Optional[str] = None

class SigningRequest:
    key_id: str
    region: str
    message: bytes
    signing_algorithm: str

class SigningResponse:
    signature: Optional[bytes] = None
    signing_algorithm: Optional[str] = None
    error: Optional[str] = None

class VerificationRequest:
    key_id: str
    region: str
    message: bytes
    signature: bytes
    signing_algorithm: str

class VerificationResponse:
    signature_valid: bool = False
    error: Optional[str] = None

class PayloadSafetyRequest:
    payload_text: str

class PayloadSafetyResponse:
    is_safe: bool
    details: Dict[str, Any]

class CryptoAuditEmbeddingRequest:
    audit_notes: str
    model_name: str = "text-embedding-004"

class CryptoAuditEmbeddingResponse:
    embedding: Optional[list[float]] = None
    error: Optional[str] = None

class ComplianceNoteTranslateRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None

class ComplianceNoteTranslateResponse:
    translated_text: Optional[str] = None
    error: Optional[str] = None
