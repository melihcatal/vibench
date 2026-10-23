"""
security_models.py - Request, response, and normalization helpers for Key Management and Encryption.

Provides Pydantic models and utility functions for normalizing encryption,
decryption, signing, verification, and audit-related payloads.
"""

import base64
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


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
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DecryptionRequest:
    ciphertext_blob: str
    encryption_context: Optional[Dict[str, str]] = None
    algorithm: str = "SYMMETRIC_DEFAULT"


@dataclass
class DecryptionResponse:
    plaintext: str
    key_id: str
    encryption_algorithm: str


@dataclass
class EnvelopeEncryptionRequest:
    plaintext: str
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class EnvelopeEncryptionResponse:
    encrypted_data_key: str
    ciphertext_blob: str
    key_id: str
    algorithm: str = "AES-GCM"


@dataclass
class SigningRequest:
    message: str
    key_id: str
    algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256"
    message_type: str = "RAW"


@dataclass
class SigningResponse:
    signature: str
    key_id: str
    signing_algorithm: str


@dataclass
class VerificationRequest:
    message: str
    signature: str
    key_id: str
    algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256"
    message_type: str = "RAW"


@dataclass
class VerificationResponse:
    is_valid: bool
    key_id: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class KeyUsageSummary:
    key_id: str
    total_operations: int
    encryption_count: int
    decryption_count: int
    signing_count: int
    verification_count: int
    date_range: Dict[str, str]
    events: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class PayloadSafetyResult:
    text: str
    is_safe: bool
    flags: List[str]
    severity: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditEmbedding:
    audit_note: str
    embedding: List[float]
    model: str
    dimensions: int
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComplianceTranslation:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    model: str
    confidence: float


def encode_ciphertext(blob: bytes) -> str:
    """Encode binary ciphertext to base64 for JSON serialization."""
    return base64.b64encode(blob).decode("utf-8")


def decode_ciphertext(encoded: str) -> bytes:
    """Decode base64 ciphertext back to bytes."""
    return base64.b64decode(encoded)


def normalize_encryption_response(raw_response: Dict[str, Any]) -> EncryptionResponse:
    """Normalize AWS KMS Encrypt API response."""
    return EncryptionResponse(
        ciphertext_blob=encode_ciphertext(raw_response["CiphertextBlob"]),
        key_id=raw_response.get("KeyId", ""),
        encryption_algorithm=raw_response.get("EncryptionAlgorithm", ""),
        metadata={
            "request_id": raw_response.get("ResponseMetadata", {}).get("RequestId", ""),
            "http_status": raw_response.get("ResponseMetadata", {}).get("HTTPStatusCode", 0),
        },
    )


def normalize_decryption_response(raw_response: Dict[str, Any]) -> DecryptionResponse:
    """Normalize AWS KMS Decrypt API response."""
    plaintext_bytes = raw_response.get("Plaintext", b"")
    if isinstance(plaintext_bytes, bytes):
        plaintext_str = plaintext_bytes.decode("utf-8")
    else:
        plaintext_str = plaintext_bytes
    return DecryptionResponse(
        plaintext=plaintext_str,
        key_id=raw_response.get("KeyId", ""),
        encryption_algorithm=raw_response.get("EncryptionAlgorithm", ""),
    )


def normalize_signing_response(raw_response: Dict[str, Any]) -> SigningResponse:
    """Normalize AWS KMS Sign API response."""
    return SigningResponse(
        signature=encode_ciphertext(raw_response["Signature"]),
        key_id=raw_response.get("KeyId", ""),
        signing_algorithm=raw_response.get("SigningAlgorithm", ""),
    )


def normalize_envelope_response(
    data_key_response: Dict[str, Any],
    encrypted_data_key: str,
    ciphertext: str,
    key_id: str,
) -> EnvelopeEncryptionResponse:
    """Normalize envelope encryption response combining KMS data key and local encryption."""
    return EnvelopeEncryptionResponse(
        encrypted_data_key=encrypted_data_key,
        ciphertext_blob=ciphertext,
        key_id=data_key_response.get("KeyId", key_id),
        algorithm="AES-GCM",
    )
