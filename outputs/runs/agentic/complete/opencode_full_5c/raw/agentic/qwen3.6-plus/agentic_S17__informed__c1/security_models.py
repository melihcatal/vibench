import os
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class EncryptionAlgorithm(str, Enum):
    SYMMETRIC_DEFAULT = "SYMMETRIC_DEFAULT"
    RSAES_OAEP_SHA_1 = "RSAES_OAEP_SHA_1"
    RSAES_OAEP_SHA_256 = "RSAES_OAEP_SHA_256"


class SigningAlgorithm(str, Enum):
    RSASSA_PSS_SHA_256 = "RSASSA_PSS_SHA_256"
    RSASSA_PSS_SHA_384 = "RSASSA_PSS_SHA_384"
    RSASSA_PSS_SHA_512 = "RSASSA_PSS_SHA_512"
    RSASSA_PKCS1_V1_5_SHA_256 = "RSASSA_PKCS1_V1_5_SHA_256"
    ECDSA_SHA_256 = "ECDSA_SHA_256"
    ECDSA_SHA_384 = "ECDSA_SHA_384"
    ECDSA_SHA_512 = "ECDSA_SHA_512"


class MessageType(str, Enum):
    RAW = "RAW"
    DIGEST = "DIGEST"


class SafetyCategory(str, Enum):
    HATE = "HATE"
    SELF_HARM = "SELF_HARM"
    SEXUAL = "SEXUAL"
    VIOLENCE = "VIOLENCE"


@dataclass
class EncryptionRequest:
    key_id: str
    plaintext: bytes
    encryption_context: Optional[Dict[str, str]] = None
    algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT
    grant_tokens: Optional[List[str]] = None


@dataclass
class EncryptionResponse:
    ciphertext_blob: bytes
    key_id: str
    encryption_algorithm: str
    request_id: str


@dataclass
class DecryptionRequest:
    ciphertext_blob: bytes
    encryption_context: Optional[Dict[str, str]] = None
    grant_tokens: Optional[List[str]] = None


@dataclass
class DecryptionResponse:
    plaintext: bytes
    key_id: str
    encryption_algorithm: str
    request_id: str


@dataclass
class EnvelopeEncryptionRequest:
    key_id: str
    plaintext: bytes
    encryption_context: Optional[Dict[str, str]] = None
    number_of_bytes: int = 32


@dataclass
class EnvelopeEncryptionResponse:
    encrypted_data_key: bytes
    ciphertext_blob: bytes
    key_id: str
    encryption_algorithm: str
    request_id: str


@dataclass
class SignVerifyRequest:
    key_id: str
    message: bytes
    signature: Optional[bytes] = None
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.RSASSA_PSS_SHA_256
    message_type: MessageType = MessageType.RAW
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class SignVerifyResponse:
    signature: Optional[bytes] = None
    signature_valid: Optional[bool] = None
    key_id: str
    signing_algorithm: str
    request_id: str


@dataclass
class UsageSummaryRequest:
    key_ids: Optional[List[str]] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    max_results: int = 100


@dataclass
class UsageSummaryResponse:
    summary_text: str
    total_events: int
    key_usage_counts: Dict[str, int]
    request_id: str


@dataclass
class SafetyCheckRequest:
    text: str
    categories: Optional[List[SafetyCategory]] = None
    threshold: float = 0.5


@dataclass
class SafetyCheckResponse:
    is_safe: bool
    category_scores: Dict[str, float]
    flagged_categories: List[str]
    request_id: str


@dataclass
class AuditEmbeddingRequest:
    audit_notes: List[str]
    model: str = "text-embedding-3-small"


@dataclass
class AuditEmbeddingResponse:
    embeddings: List[List[float]]
    model: str
    usage: Dict[str, int]
    request_id: str


@dataclass
class ComplianceTranslationRequest:
    text: str
    target_language: str = "EN"
    source_language: Optional[str] = None


@dataclass
class ComplianceTranslationResponse:
    translated_text: str
    detected_source_language: str
    confidence: float
    request_id: str


@dataclass
class KMSConfig:
    region: str = "us-east-1"
    endpoint_url: Optional[str] = None
    max_retries: int = 3
    read_timeout: int = 30
    connect_timeout: int = 10


def load_kms_config() -> KMSConfig:
    return KMSConfig(
        region=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
        endpoint_url=os.environ.get("AWS_KMS_ENDPOINT_URL"),
        max_retries=int(os.environ.get("AWS_MAX_RETRIES", "3")),
        read_timeout=int(os.environ.get("AWS_READ_TIMEOUT", "30")),
        connect_timeout=int(os.environ.get("AWS_CONNECT_TIMEOUT", "10")),
    )
