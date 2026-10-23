import os
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
from enum import Enum
from datetime import datetime


class EncryptionAlgorithm(str, Enum):
    SYMMETRIC_DEFAULT = "SYMMETRIC_DEFAULT"
    RSAES_OAEP_SHA_1 = "RSAES_OAEP_SHA_1"
    RSAES_OAEP_SHA_256 = "RSAES_OAEP_SHA_256"


class SigningAlgorithm(str, Enum):
    RSASSA_PKCS1_V1_5_SHA_256 = "RSASSA_PKCS1_V1_5_SHA_256"
    RSASSA_PKCS1_V1_5_SHA_384 = "RSASSA_PKCS1_V1_5_SHA_384"
    RSASSA_PKCS1_V1_5_SHA_512 = "RSASSA_PKCS1_V1_5_SHA_512"
    RSASSA_PSS_SHA_256 = "RSASSA_PSS_SHA_256"
    RSASSA_PSS_SHA_384 = "RSASSA_PSS_SHA_384"
    RSASSA_PSS_SHA_512 = "RSASSA_PSS_SHA_512"
    ECDSA_SHA_256 = "ECDSA_SHA_256"
    ECDSA_SHA_384 = "ECDSA_SHA_384"
    ECDSA_SHA_512 = "ECDSA_SHA_512"


class MessageType(str, Enum):
    RAW = "RAW"
    DIGEST = "DIGEST"


class KeySpec(str, Enum):
    SYMMETRIC_DEFAULT = "SYMMETRIC_DEFAULT"
    RSA_2048 = "RSA_2048"
    RSA_3072 = "RSA_3072"
    RSA_4096 = "RSA_4096"
    ECC_NIST_P256 = "ECC_NIST_P256"
    ECC_NIST_P384 = "ECC_NIST_P384"
    ECC_NIST_P521 = "ECC_NIST_P521"


@dataclass
class EncryptRequest:
    key_id: str
    plaintext: bytes
    encryption_context: Optional[Dict[str, str]] = None
    encryption_algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT
    grant_tokens: Optional[List[str]] = None


@dataclass
class EncryptResponse:
    ciphertext_blob: bytes
    key_id: str
    encryption_algorithm: str
    request_id: str
    http_status_code: int


@dataclass
class DecryptRequest:
    ciphertext_blob: bytes
    encryption_context: Optional[Dict[str, str]] = None
    grant_tokens: Optional[List[str]] = None
    encryption_algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT


@dataclass
class DecryptResponse:
    plaintext: bytes
    key_id: str
    encryption_algorithm: str
    request_id: str
    http_status_code: int


@dataclass
class EnvelopeEncryptRequest:
    key_id: str
    plaintext: bytes
    encryption_context: Optional[Dict[str, str]] = None
    number_of_bytes: int = 32
    encryption_algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT


@dataclass
class EnvelopeEncryptResponse:
    encrypted_data_key: bytes
    ciphertext_blob: bytes
    key_id: str
    encryption_context: Dict[str, str]
    request_id: str
    http_status_code: int


@dataclass
class SignRequest:
    key_id: str
    message: bytes
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256
    message_type: MessageType = MessageType.RAW
    encryption_context: Optional[Dict[str, str]] = None
    grant_tokens: Optional[List[str]] = None


@dataclass
class SignResponse:
    signature: bytes
    key_id: str
    signing_algorithm: str
    request_id: str
    http_status_code: int


@dataclass
class VerifyRequest:
    key_id: str
    message: bytes
    signature: bytes
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256
    message_type: MessageType = MessageType.RAW
    encryption_context: Optional[Dict[str, str]] = None
    grant_tokens: Optional[List[str]] = None


@dataclass
class VerifyResponse:
    signature_valid: bool
    key_id: str
    signing_algorithm: str
    request_id: str
    http_status_code: int


@dataclass
class KeyUsageSummary:
    key_id: str
    key_state: str
    key_usage: str
    encryption_count: int = 0
    decryption_count: int = 0
    sign_count: int = 0
    verify_count: int = 0
    generate_data_key_count: int = 0
    last_used: Optional[datetime] = None
    created_at: Optional[datetime] = None
    description: str = ""


@dataclass
class PayloadSafetyFlag:
    category: str
    severity: str
    detail: str
    confidence: float


@dataclass
class PayloadSafetyResult:
    is_safe: bool
    flags: List[PayloadSafetyFlag] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class AuditEmbedding:
    text: str
    embedding: List[float]
    model: str
    usage: Dict[str, int] = field(default_factory=dict)


@dataclass
class ComplianceNoteTranslation:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    model: str
    usage: Dict[str, int] = field(default_factory=dict)


def normalize_plaintext(data: Any) -> bytes:
    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        return data.encode("utf-8")
    if isinstance(data, (dict, list)):
        import json

        return json.dumps(data, sort_keys=True).encode("utf-8")
    return str(data).encode("utf-8")


def normalize_ciphertext(data: Any) -> bytes:
    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        import base64

        try:
            return base64.b64decode(data)
        except Exception:
            return data.encode("utf-8")
    raise TypeError("Ciphertext must be bytes or base64-encoded string")


def format_ciphertext_for_storage(ciphertext: bytes) -> str:
    import base64

    return base64.b64encode(ciphertext).decode("utf-8")
