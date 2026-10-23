"""
Local request, response, and normalization helpers for Key Management and Encryption.

Provides dataclasses and utility functions for normalizing cryptographic
operations across AWS KMS integration workflows.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum
import base64
import json


class KeyPurpose(str, Enum):
    ENCRYPT_DECRYPT = "ENCRYPT_DECRYPT"
    SIGN_VERIFY = "SIGN_VERIFY"


class KeyState(str, Enum):
    ENABLED = "Enabled"
    DISABLED = "Disabled"
    PENDING_DELETION = "PendingDeletion"


@dataclass
class EncryptionRequest:
    plaintext: str
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None
    grant_tokens: Optional[List[str]] = None


@dataclass
class EncryptionResponse:
    ciphertext_blob: str  # base64 encoded
    key_id: str
    encryption_algorithm: str = "SYMMETRIC_DEFAULT"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DecryptionRequest:
    ciphertext_blob: str
    key_id: Optional[str] = None
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class DecryptionResponse:
    plaintext: str
    key_id: str
    encryption_algorithm: str = "SYMMETRIC_DEFAULT"


@dataclass
class EnvelopeEncryptionRequest:
    plaintext: str
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class EnvelopeEncryptionResponse:
    encrypted_data_key: str  # base64 encoded
    encrypted_payload: str  # base64 encoded
    key_id: str
    algorithm: str = "AES-256-GCM"


@dataclass
class EnvelopeDecryptionRequest:
    encrypted_data_key: str
    encrypted_payload: str
    key_id: Optional[str] = None


@dataclass
class SigningRequest:
    message: str
    key_id: str
    message_type: str = "RAW"
    signing_algorithm: str = "RSASSA_PSS_SHA_256"


@dataclass
class SigningResponse:
    signature: str  # base64 encoded
    key_id: str
    signing_algorithm: str


@dataclass
class VerificationRequest:
    message: str
    signature: str
    key_id: str
    signing_algorithm: str = "RSASSA_PSS_SHA_256"


@dataclass
class VerificationResponse:
    is_valid: bool
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
    result: str = "success"


@dataclass
class KeyUsageSummary:
    key_id: str
    total_operations: int
    encrypt_count: int = 0
    decrypt_count: int = 0
    sign_count: int = 0
    verify_count: int = 0
    unique_users: int = 0
    event_log: List[KeyUsageEvent] = field(default_factory=list)


@dataclass
class AuditNoteRequest:
    note_text: str
    key_id: Optional[str] = None
    event_type: str = "audit"


@dataclass
class EmbeddingResponse:
    vector: List[float]
    model: str
    text: str
    usage: Dict[str, int]


@dataclass
class ComplianceTranslationRequest:
    text: str
    target_language: str
    source_language: str = "en"


@dataclass
class ComplianceTranslationResponse:
    translated_text: str
    target_language: str
    source_language: str
    model: str


def normalize_base64(data: bytes) -> str:
    """Encode bytes to base64 string for JSON serialization."""
    return base64.b64encode(data).decode("utf-8")


def denormalize_base64(data: str) -> bytes:
    """Decode base64 string to bytes."""
    return base64.b64decode(data)


def normalize_key_id(key_id: str) -> str:
    """Normalize AWS KMS key identifier formats."""
    if key_id.startswith("arn:aws:kms:"):
        return key_id
    if key_id.startswith("mrk-"):
        return key_id
    if len(key_id) == 36 and key_id.count("-") == 4:
        return key_id
    return key_id


def serialize_encryption_context(ctx: Optional[Dict[str, str]]) -> Dict[str, str]:
    """Ensure encryption context values are strings for AWS KMS."""
    if ctx is None:
        return {}
    return {str(k): str(v) for k, v in ctx.items()}


def build_key_usage_from_events(key_id: str, events: List[Dict[str, Any]]) -> KeyUsageSummary:
    """Build a KeyUsageSummary from a list of event dictionaries."""
    summary = KeyUsageSummary(key_id=key_id, total_operations=len(events))
    unique_users = set()

    for event in events:
        event_obj = KeyUsageEvent(
            timestamp=event.get("eventTime", ""),
            event_name=event.get("eventName", ""),
            key_id=event.get("resources", [{}])[0].get("ARN", key_id) if event.get("resources") else key_id,
            user_identity=event.get("userIdentity", {}).get("arn", "unknown"),
            source_ip=event.get("sourceIPAddress", ""),
            region=event.get("awsRegion", ""),
            result="success" if event.get("errorCode") is None else "failed",
        )
        summary.event_log.append(event_obj)
        unique_users.add(event_obj.user_identity)

        event_lower = event_obj.event_name.lower()
        if "encrypt" in event_lower and "decrypt" not in event_lower:
            summary.encrypt_count += 1
        elif "decrypt" in event_lower:
            summary.decrypt_count += 1
        elif "sign" in event_lower and "verify" not in event_lower:
            summary.sign_count += 1
        elif "verify" in event_lower:
            summary.verify_count += 1

    summary.unique_users = len(unique_users)
    return summary
