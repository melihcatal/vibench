"""
Local request, response, and normalization helpers for Key Management and Encryption.
Provides data models and utility functions for security payload handling.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime
import base64
import json


@dataclass
class EncryptionRequest:
    """Normalized encryption request model."""
    key_id: str
    plaintext: str
    encryption_context: Optional[Dict[str, str]] = None
    algorithm: str = "SYMMETRIC_DEFAULT"

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "KeyId": self.key_id,
            "Plaintext": self.plaintext.encode("utf-8"),
        }
        if self.encryption_context:
            result["EncryptionContext"] = self.encryption_context
        return result


@dataclass
class EncryptionResponse:
    """Normalized encryption response model."""
    ciphertext_blob: bytes
    key_id: str
    encryption_algorithm: str
    response_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_base64(self) -> str:
        return base64.b64encode(self.ciphertext_blob).decode("utf-8")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ciphertext_blob": self.to_base64(),
            "key_id": self.key_id,
            "encryption_algorithm": self.encryption_algorithm,
            "response_metadata": self.response_metadata,
        }


@dataclass
class DecryptionRequest:
    """Normalized decryption request model."""
    ciphertext_blob: bytes
    encryption_context: Optional[Dict[str, str]] = None

    @classmethod
    def from_base64(cls, ciphertext_b64: str, encryption_context: Optional[Dict[str, str]] = None):
        return cls(
            ciphertext_blob=base64.b64decode(ciphertext_b64),
            encryption_context=encryption_context,
        )


@dataclass
class DecryptionResponse:
    """Normalized decryption response model."""
    plaintext: bytes
    key_id: str
    response_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_text(self) -> str:
        return self.plaintext.decode("utf-8")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plaintext": self.to_text(),
            "key_id": self.key_id,
            "response_metadata": self.response_metadata,
        }


@dataclass
class EnvelopeEncryptionRequest:
    """Envelope encryption request model."""
    key_id: str
    plaintext: str
    data_key_spec: str = "AES_256"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "KeyId": self.key_id,
            "KeySpec": self.data_key_spec,
            "Plaintext": self.plaintext.encode("utf-8"),
        }


@dataclass
class EnvelopeEncryptionResponse:
    """Envelope encryption response model."""
    plaintext_data_key: bytes
    encrypted_data_key: bytes
    ciphertext: bytes
    key_id: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "encrypted_data_key": base64.b64encode(self.encrypted_data_key).decode("utf-8"),
            "ciphertext": base64.b64encode(self.ciphertext).decode("utf-8"),
            "key_id": self.key_id,
        }


@dataclass
class SigningRequest:
    """Digital signing request model."""
    key_id: str
    message: bytes
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256"


@dataclass
class SigningResponse:
    """Digital signing response model."""
    signature: bytes
    key_id: str
    signing_algorithm: str
    response_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_base64(self) -> str:
        return base64.b64encode(self.signature).decode("utf-8")


@dataclass
class VerificationRequest:
    """Signature verification request model."""
    key_id: str
    message: bytes
    signature: bytes
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256"


@dataclass
class VerificationResponse:
    """Signature verification response model."""
    is_valid: bool
    key_id: str
    response_metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyUsageEvent:
    """Represents a single key usage event."""
    timestamp: datetime
    key_id: str
    operation: str
    success: bool
    details: Optional[Dict[str, Any]] = None


@dataclass
class KeyUsageSummary:
    """Aggregated key usage summary."""
    key_id: str
    total_operations: int
    successful_operations: int
    failed_operations: int
    operations_by_type: Dict[str, int]
    time_range: Optional[tuple] = None
    events: List[KeyUsageEvent] = field(default_factory=list)


def normalize_encryption_context(context: Optional[Dict[str, Any]]) -> Optional[Dict[str, str]]:
    """Normalize encryption context to string key-value pairs."""
    if context is None:
        return None
    return {str(k): str(v) for k, v in context.items()}


def format_audit_note(operation: str, key_id: str, success: bool, details: str = "") -> str:
    """Format a crypto audit note for logging or embedding."""
    status = "SUCCESS" if success else "FAILED"
    return f"[{status}] Key {key_id} - Operation: {operation} - {details}"
