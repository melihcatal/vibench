import dataclasses
from typing import Dict, Any, Optional

@dataclasses.dataclass
class EncryptionRequest:
    key_id: str
    plaintext: str

@dataclasses.dataclass
class EncryptionResponse:
    ciphertext: bytes
    key_id: str

@dataclasses.dataclass
class DecryptionRequest:
    ciphertext: bytes
    key_id: Optional[str] = None

@dataclasses.dataclass
class DecryptionResponse:
    plaintext: str
    key_id: str

@dataclasses.dataclass
class EnvelopeEncryptionRequest:
    key_id: str
    plaintext: str

@dataclasses.dataclass
class EnvelopeEncryptionResponse:
    ciphertext_blob: bytes
    encrypted_data_key: bytes
    key_id: str

@dataclasses.dataclass
class SignRequest:
    key_id: str
    message: bytes
    signing_algorithm: str

@dataclasses.dataclass
class SignResponse:
    signature: bytes
    key_id: str
    signing_algorithm: str

@dataclasses.dataclass
class VerifyRequest:
    key_id: str
    message: bytes
    signature: bytes
    signing_algorithm: str

@dataclasses.dataclass
class VerifyResponse:
    signature_valid: bool
    key_id: str

@dataclasses.dataclass
class KeyUsageEvent:
    event_id: str
    event_name: str
    event_time: str
    key_id: str
    source_ip_address: str
    user_identity: Dict[str, Any]

@dataclasses.dataclass
class PayloadSafetyScanRequest:
    text_payload: str
    language_code: str = "en"

@dataclasses.dataclass
class PayloadSafetyScanResponse:
    unsafe_content_found: bool
    details: Dict[str, Any]

@dataclasses.dataclass
class CryptoAuditEmbeddingRequest:
    audit_note: str

@dataclasses.dataclass
class CryptoAuditEmbeddingResponse:
    embedding: list[float]

@dataclasses.dataclass
class ComplianceNoteTranslateRequest:
    text: str
    source_language_code: str
    target_language_code: str

@dataclasses.dataclass
class ComplianceNoteTranslateResponse:
    translated_text: str
    source_language_code: str
    target_language_code: str
