from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any


@dataclass
class EncryptRequest:
    key_id: str
    plaintext: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class EncryptResponse:
    ciphertext: str
    key_id: str
    encryption_algorithm: str
    request_id: str


@dataclass
class DecryptRequest:
    key_id: Optional[str]
    ciphertext_blob: bytes
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class DecryptResponse:
    plaintext: str
    key_id: str
    encryption_algorithm: str
    request_id: str


@dataclass
class EnvelopeEncryptRequest:
    key_id: str
    plaintext: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class EnvelopeEncryptResponse:
    encrypted_data_key: str
    nonce: str
    ciphertext: str
    key_id: str
    encryption_algorithm: str
    request_id: str


@dataclass
class SignRequest:
    key_id: str
    message: bytes
    signing_algorithm: str = "RSASSA_PSS_SHA_256"


@dataclass
class SignResponse:
    signature: str
    key_id: str
    signing_algorithm: str
    request_id: str


@dataclass
class VerifyRequest:
    key_id: str
    message: bytes
    signature: bytes
    signing_algorithm: str = "RSASSA_PSS_SHA_256"


@dataclass
class VerifyResponse:
    signature_valid: bool
    key_id: str
    signing_algorithm: str
    request_id: str


@dataclass
class KeyUsageEvent:
    key_id: str
    event_name: str
    event_time: str
    user_identity: str
    source_ip: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class KeyUsageSummary:
    key_id: str
    total_operations: int
    encrypt_count: int
    decrypt_count: int
    generate_data_key_count: int
    sign_count: int
    verify_count: int
    events: List[KeyUsageEvent] = field(default_factory=list)


@dataclass
class PayloadSafetyResult:
    text: str
    is_safe: bool
    findings: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class AuditEmbedding:
    text: str
    embedding: List[float]
    model_id: str
    token_count: int


@dataclass
class ComplianceTranslation:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str
    model_id: str


def normalize_key_id(key_id: str) -> str:
    if key_id.startswith("arn:aws:kms:"):
        return key_id
    if key_id.startswith("alias/"):
        return key_id
    return key_id


def normalize_encryption_context(context: Optional[Dict[str, str]]) -> Dict[str, str]:
    if context is None:
        return {}
    return {str(k): str(v) for k, v in context.items()}
