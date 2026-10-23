from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class EncryptionRequest:
    plaintext: str
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None
    algorithm: str = "SYMMETRIC_DEFAULT"


@dataclass
class EncryptionResponse:
    ciphertext_blob: str
    key_id: str
    encryption_algorithm: str
    request_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DecryptionRequest:
    ciphertext_blob: str
    key_id: Optional[str] = None
    encryption_context: Optional[Dict[str, str]] = None
    algorithm: str = "SYMMETRIC_DEFAULT"


@dataclass
class DecryptionResponse:
    plaintext: str
    key_id: str
    encryption_algorithm: str
    request_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EnvelopeEncryptionRequest:
    plaintext: str
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None
    data_key_spec: str = "AES_256"


@dataclass
class EnvelopeEncryptionResponse:
    encrypted_data_key: str
    ciphertext_blob: str
    plaintext_data_key: str
    key_id: str
    algorithm: str
    request_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SigningRequest:
    message: str
    key_id: str
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256"
    message_type: str = "RAW"


@dataclass
class SigningResponse:
    signature: str
    key_id: str
    signing_algorithm: str
    request_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VerificationRequest:
    message: str
    signature: str
    key_id: str
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256"
    message_type: str = "RAW"


@dataclass
class VerificationResponse:
    valid: bool
    key_id: str
    signing_algorithm: str
    request_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyUsageSummaryRequest:
    key_id: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    operation_filter: Optional[List[str]] = None


@dataclass
class KeyUsageEvent:
    timestamp: str
    operation: str
    key_id: str
    status: str
    encryption_context: Optional[Dict[str, str]] = None
    request_id: Optional[str] = None


@dataclass
class KeyUsageSummaryResponse:
    key_id: str
    total_operations: int
    operations_by_type: Dict[str, int]
    events: List[KeyUsageEvent]
    period_start: str
    period_end: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PayloadSafetyRequest:
    text: str
    categories: Optional[List[str]] = None
    threshold: float = 0.5


@dataclass
class SafetyCategoryResult:
    category: str
    score: float
    flagged: bool


@dataclass
class PayloadSafetyResponse:
    safe: bool
    categories: List[SafetyCategoryResult]
    overall_score: float
    request_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditEmbeddingRequest:
    audit_notes: List[str]
    model: str = "text-embedding-3-small"


@dataclass
class AuditEmbeddingResult:
    text: str
    embedding: List[float]
    index: int


@dataclass
class AuditEmbeddingResponse:
    embeddings: List[AuditEmbeddingResult]
    model: str
    total_tokens: int
    request_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComplianceTranslationRequest:
    text: str
    source_language: str = "en"
    target_language: str = "es"
    model: Optional[str] = None


@dataclass
class ComplianceTranslationResponse:
    translated_text: str
    source_language: str
    target_language: str
    detected_language: str
    request_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)
