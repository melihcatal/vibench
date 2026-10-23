"""
Local request, response, and normalization helpers for Key Management and Encryption.
Defines data models and normalization utilities shared across KMS operations.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime


# ---------------------------------------------------------------------------
# Request Models
# ---------------------------------------------------------------------------

@dataclass
class EncryptRequest:
    """Parameters for an encrypt operation."""
    plaintext: bytes
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None
    grant_tokens: Optional[List[str]] = None


@dataclass
class DecryptRequest:
    """Parameters for a decrypt operation."""
    ciphertext: bytes
    key_id: Optional[str] = None
    encryption_context: Optional[Dict[str, str]] = None
    grant_tokens: Optional[List[str]] = None
    recipient: Optional[Dict[str, str]] = None


@dataclass
class EnvelopeEncryptRequest:
    """Parameters for envelope encryption."""
    plaintext: bytes
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None
    data_key_spec: str = "AES_256"


@dataclass
class SignRequest:
    """Parameters for a signing operation."""
    message: bytes
    key_id: str
    message_type: str = "RAW"  # RAW or DIGEST
    signing_algorithm: Optional[str] = None


@dataclass
class VerifyRequest:
    """Parameters for a signature verification operation."""
    message: bytes
    signature: bytes
    key_id: str
    message_type: str = "RAW"
    signing_algorithm: Optional[str] = None


# ---------------------------------------------------------------------------
# Response Models
# ---------------------------------------------------------------------------

@dataclass
class EncryptResponse:
    """Result of an encrypt operation."""
    ciphertext: bytes
    key_id: str
    encryption_algorithm: str = "SYMMETRIC_DEFAULT"
    request_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DecryptResponse:
    """Result of a decrypt operation."""
    plaintext: bytes
    key_id: str
    encryption_algorithm: str = "SYMMETRIC_DEFAULT"
    request_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EnvelopeEncryptResponse:
    """Result of an envelope encryption operation."""
    encrypted_data_key: bytes
    ciphertext: bytes
    key_id: str
    data_key_spec: str = "AES_256"
    request_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SignResponse:
    """Result of a signing operation."""
    signature: bytes
    key_id: str
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256"
    request_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VerifyResponse:
    """Result of a signature verification operation."""
    signature_valid: bool
    key_id: str
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256"
    request_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Normalization Helpers
# ---------------------------------------------------------------------------

def normalize_encryption_context(
    context: Optional[Dict[str, str]],
) -> Dict[str, str]:
    """Ensure encryption context values are strings."""
    if context is None:
        return {}
    return {str(k): str(v) for k, v in context.items()}


def normalize_kms_response(raw_response: dict) -> Dict[str, Any]:
    """Extract and normalize fields from a raw AWS KMS API response dict."""
    result: Dict[str, Any] = {}
    if "KeyId" in raw_response:
        result["key_id"] = raw_response["KeyId"]
    if "RequestId" in raw_response:
        result["request_id"] = raw_response["RequestId"]
    if "EncryptionAlgorithm" in raw_response:
        result["encryption_algorithm"] = raw_response["EncryptionAlgorithm"]
    if "SigningAlgorithm" in raw_response:
        result["signing_algorithm"] = raw_response["SigningAlgorithm"]
    result["metadata"] = {
        k: v for k, v in raw_response.items()
        if k not in (
            "KeyId", "RequestId", "CiphertextBlob", "Plaintext",
            "EncryptionAlgorithm", "SigningAlgorithm", "Signature",
            "SignatureValid",
        )
    }
    return result


def format_key_usage_record(
    key_id: str,
    operation: str,
    timestamp: Optional[datetime] = None,
    success: bool = True,
    error_message: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a normalized key usage record dict."""
    record: Dict[str, Any] = {
        "key_id": key_id,
        "operation": operation,
        "timestamp": (timestamp or datetime.utcnow()).isoformat(),
        "success": success,
    }
    if error_message:
        record["error_message"] = error_message
    return record
