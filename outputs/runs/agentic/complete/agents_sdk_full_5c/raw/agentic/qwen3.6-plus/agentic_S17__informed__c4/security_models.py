"""Local request, response, and normalization helpers for Key Management and Encryption."""

from dataclasses import dataclass, field
from typing import Optional, List, Dict


@dataclass
class EncryptRequest:
    plaintext: bytes
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class EncryptResponse:
    ciphertext: bytes
    key_id: str
    algorithm: str
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class DecryptRequest:
    ciphertext: bytes
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class DecryptResponse:
    plaintext: bytes
    key_id: str
    encryption_algorithm: str


@dataclass
class GenerateDataKeyRequest:
    key_id: str
    key_spec: str = "AES_256"
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class EnvelopeEncryptRequest:
    plaintext: bytes
    key_id: str
    key_spec: str = "AES_256"
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class EnvelopeEncryptResponse:
    encrypted_data_key: bytes
    ciphertext: bytes
    key_id: str
    algorithm: str
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class SignRequest:
    message: bytes
    key_id: str
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256"
    message_type: str = "RAW"


@dataclass
class SignResponse:
    signature: bytes
    key_id: str
    signing_algorithm: str


@dataclass
class VerifyRequest:
    message: bytes
    signature: bytes
    key_id: str
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256"
    message_type: str = "RAW"


@dataclass
class VerifyResponse:
    valid: bool
    key_id: str
    signing_algorithm: str


@dataclass
class KeyUsageEvent:
    timestamp: str
    event_name: str
    key_id: str
    user_identity: str
    source_ip: str
    region: str


@dataclass
class KeyUsageSummary:
    key_id: str
    total_operations: int
    encrypt_count: int
    decrypt_count: int
    sign_count: int
    verify_count: int
    generate_data_key_count: int
    recent_events: List[KeyUsageEvent] = field(default_factory=list)


@dataclass
class SafetyCheckRequest:
    text: str


@dataclass
class SafetyViolation:
    category: str
    severity: str
    score: float
    detail: str


@dataclass
class SafetyCheckResponse:
    is_safe: bool
    violations: List[SafetyViolation] = field(default_factory=list)
    raw_result: Optional[Dict] = None


@dataclass
class EmbedRequest:
    text: str
    model: str = "text-embedding-3-small"


@dataclass
class EmbedResponse:
    embedding: List[float]
    model: str
    text: str
    token_count: int = 0


@dataclass
class TranslateRequest:
    text: str
    source_lang: str = "auto"
    target_lang: str = "en"


@dataclass
class TranslateResponse:
    translated_text: str
    source_lang: str
    target_lang: str


def normalize_encrypt_response(raw: dict) -> EncryptResponse:
    return EncryptResponse(
        ciphertext=raw.get("ciphertext_blob", b""),
        key_id=raw.get("key_id", ""),
        algorithm=raw.get("encryption_algorithm", ""),
        encryption_context=raw.get("encryption_context"),
    )


def normalize_decrypt_response(raw: dict) -> DecryptResponse:
    return DecryptResponse(
        plaintext=raw.get("plaintext", b""),
        key_id=raw.get("key_id", ""),
        encryption_algorithm=raw.get("encryption_algorithm", ""),
    )


def normalize_envelope_response(raw: dict) -> EnvelopeEncryptResponse:
    return EnvelopeEncryptResponse(
        encrypted_data_key=raw.get("encrypted_data_key", b""),
        ciphertext=raw.get("ciphertext", b""),
        key_id=raw.get("key_id", ""),
        algorithm=raw.get("algorithm", ""),
        encryption_context=raw.get("encryption_context"),
    )


def normalize_sign_response(raw: dict) -> SignResponse:
    return SignResponse(
        signature=raw.get("signature", b""),
        key_id=raw.get("key_id", ""),
        signing_algorithm=raw.get("signing_algorithm", ""),
    )


def normalize_verify_response(raw: dict) -> VerifyResponse:
    return VerifyResponse(
        valid=raw.get("signature_valid", False),
        key_id=raw.get("key_id", ""),
        signing_algorithm=raw.get("signing_algorithm", ""),
    )
