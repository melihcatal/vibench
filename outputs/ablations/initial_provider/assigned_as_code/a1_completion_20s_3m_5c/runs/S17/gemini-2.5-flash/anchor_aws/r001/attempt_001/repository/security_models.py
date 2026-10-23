from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class EncryptionRequest:
    plaintext: bytes
    key_id: str
    region: str

@dataclass
class EncryptionResponse:
    ciphertext: bytes
    key_id: str
    region: str

@dataclass
class DecryptionRequest:
    ciphertext: bytes
    key_id: str
    region: str

@dataclass
class DecryptionResponse:
    plaintext: bytes
    key_id: str
    region: str

@dataclass
class EnvelopeEncryptionRequest:
    plaintext: bytes
    key_id: str
    region: str
    encryption_context: Optional[Dict[str, str]] = None

@dataclass
class EnvelopeEncryptionResponse:
    ciphertext_blob: bytes
    plaintext_data_key: bytes
    ciphertext_data_key: bytes
    key_id: str
    region: str

@dataclass
class SignRequest:
    message: bytes
    key_id: str
    region: str
    signing_algorithm: str

@dataclass
class SignResponse:
    signature: bytes
    key_id: str
    region: str
    signing_algorithm: str

@dataclass
class VerifyRequest:
    message: bytes
    signature: bytes
    key_id: str
    region: str
    signing_algorithm: str

@dataclass
class VerifyResponse:
    signature_valid: bool
    key_id: str
    region: str

@dataclass
class KeyUsageSummaryRequest:
    start_time: str
    end_time: str
    region: str
    key_id: Optional[str] = None

@dataclass
class KeyUsageSummaryResponse:
    summary_data: Dict[str, Any]

@dataclass
class PayloadSafetyRequest:
    text_payload: str
    region: str

@dataclass
class PayloadSafetyResponse:
    unsafe_content_detected: bool
    findings: Dict[str, Any]

@dataclass
class CryptoAuditEmbeddingRequest:
    audit_note: str
    region: str

@dataclass
class CryptoAuditEmbeddingResponse:
    embedding_vector: list[float]

@dataclass
class ComplianceNoteTranslateRequest:
    text: str
    source_language_code: str
    target_language_code: str
    region: str

@dataclass
class ComplianceNoteTranslateResponse:
    translated_text: str
    source_language_code: str
    target_language_code: str
