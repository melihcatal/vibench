import os
import base64
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum


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


class KeySpec(str, Enum):
    SYMMETRIC_DEFAULT = "SYMMETRIC_DEFAULT"
    RSA_2048 = "RSA_2048"
    RSA_3072 = "RSA_3072"
    RSA_4096 = "RSA_4096"
    ECC_NIST_P256 = "ECC_NIST_P256"
    ECC_NIST_P384 = "ECC_NIST_P384"
    ECC_NIST_P521 = "ECC_NIST_P521"


class MessageType(str, Enum):
    RAW = "RAW"
    DIGEST = "DIGEST"


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
    encryption_algorithm: Optional[EncryptionAlgorithm] = None


@dataclass
class DecryptResponse:
    plaintext: bytes
    key_id: str
    encryption_algorithm: str
    request_id: str
    http_status_code: int


@dataclass
class GenerateDataKeyRequest:
    key_id: str
    key_spec: Optional[str] = None
    number_of_bytes: Optional[int] = None
    encryption_context: Optional[Dict[str, str]] = None
    grant_tokens: Optional[List[str]] = None


@dataclass
class GenerateDataKeyResponse:
    plaintext_data_key: bytes
    encrypted_data_key: bytes
    key_id: str
    request_id: str
    http_status_code: int


@dataclass
class SignRequest:
    key_id: str
    message: bytes
    signing_algorithm: SigningAlgorithm
    message_type: MessageType = MessageType.RAW
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
    signing_algorithm: SigningAlgorithm
    message_type: MessageType = MessageType.RAW
    grant_tokens: Optional[List[str]] = None


@dataclass
class VerifyResponse:
    signature_valid: bool
    key_id: str
    signing_algorithm: str
    request_id: str
    http_status_code: int


@dataclass
class EnvelopeEncryptionResult:
    encrypted_data_key: bytes
    encrypted_payload: bytes
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class EnvelopeDecryptionResult:
    plaintext: bytes
    key_id: str


@dataclass
class KeyUsageSummary:
    key_id: str
    total_encryptions: int = 0
    total_decryptions: int = 0
    total_signs: int = 0
    total_verifications: int = 0
    total_data_key_generations: int = 0
    last_used_timestamp: Optional[str] = None
    key_state: Optional[str] = None
    key_rotation_enabled: bool = False


@dataclass
class SafetyCheckResult:
    is_safe: bool
    categories_flagged: List[str] = field(default_factory=list)
    severity_scores: Dict[str, float] = field(default_factory=dict)
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class EmbeddingResult:
    text: str
    embedding: List[float]
    model: str
    token_count: Optional[int] = None


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str
    model: Optional[str] = None


def normalize_plaintext(plaintext: str) -> bytes:
    if isinstance(plaintext, str):
        return plaintext.encode("utf-8")
    return plaintext


def normalize_ciphertext(ciphertext: str) -> bytes:
    if isinstance(ciphertext, str):
        return base64.b64decode(ciphertext)
    return ciphertext


def encode_ciphertext(ciphertext: bytes) -> str:
    if isinstance(ciphertext, bytes):
        return base64.b64encode(ciphertext).decode("utf-8")
    return ciphertext


def encode_signature(signature: bytes) -> str:
    if isinstance(signature, bytes):
        return base64.b64encode(signature).decode("utf-8")
    return signature


def decode_signature(signature: str) -> bytes:
    if isinstance(signature, str):
        return base64.b64decode(signature)
    return signature


def build_encryption_context(**kwargs: str) -> Dict[str, str]:
    return {k: v for k, v in kwargs.items() if v}


def validate_key_id(key_id: str) -> str:
    if not key_id or not key_id.strip():
        raise ValueError("key_id must be a non-empty string")
    return key_id.strip()


def validate_plaintext(plaintext: bytes) -> bytes:
    if not plaintext:
        raise ValueError("plaintext must be non-empty bytes")
    if len(plaintext) > 4096:
        raise ValueError("plaintext exceeds 4096 byte limit for direct KMS encryption")
    return plaintext
