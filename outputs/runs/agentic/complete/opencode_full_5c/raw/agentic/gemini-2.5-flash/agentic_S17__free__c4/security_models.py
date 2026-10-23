from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class EncryptRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    plaintext: str


@dataclass
class EncryptResponse:
    ciphertext: str


@dataclass
class DecryptRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    ciphertext: str


@dataclass
class DecryptResponse:
    plaintext: str


@dataclass
class EnvelopeEncryptRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    plaintext: str


@dataclass
class EnvelopeEncryptResponse:
    encrypted_data_key: str
    ciphertext: str


@dataclass
class SignRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    message: str


@dataclass
class SignResponse:
    signature: str


@dataclass
class VerifyRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    message: str
    signature: str


@dataclass
class VerifyResponse:
    is_valid: bool


@dataclass
class KeyUsageSummaryRequest:
    project_id: str
    filter: Optional[str] = None
    page_size: Optional[int] = None
    page_token: Optional[str] = None


@dataclass
class KeyUsageSummaryResponse:
    log_entries: List[Dict[str, Any]]
    next_page_token: Optional[str] = None


@dataclass
class PayloadSafetyRequest:
    project_id: str
    content: str
    location_id: str = "global"


@dataclass
class PayloadSafetyResponse:
    has_unsafe_content: bool
    findings: List[Dict[str, Any]]


@dataclass
class CryptoAuditEmbeddingRequest:
    project_id: str
    location_id: str
    document_content: str


@dataclass
class CryptoAuditEmbeddingResponse:
    embedding: List[float]


@dataclass
class ComplianceNoteTranslateRequest:
    project_id: str
    location_id: str
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None


@dataclass
class ComplianceNoteTranslateResponse:
    translated_text: str
    detected_language_code: Optional[str] = None
