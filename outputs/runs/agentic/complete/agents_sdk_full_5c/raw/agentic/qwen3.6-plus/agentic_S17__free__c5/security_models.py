"""
security_models.py - Define local request, response, and normalization helpers
for Key Management and Encryption operations.
"""

from __future__ import annotations

import base64
import dataclasses
from typing import Any, Dict, List, Optional


@dataclasses.dataclass
class EncryptRequest:
    """Normalized request for encrypting a payload."""
    plaintext: str
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None
    grant_tokens: Optional[List[str]] = None


@dataclasses.dataclass
class EncryptResponse:
    """Normalized response from an encryption operation."""
    ciphertext_blob: str  # base64-encoded
    key_id: str
    encryption_algorithm: Optional[str] = None
    ciphertext_type: Optional[str] = None


@dataclasses.dataclass
class DecryptRequest:
    """Normalized request for decrypting a payload."""
    ciphertext_blob: str
    encryption_context: Optional[Dict[str, str]] = None
    grant_tokens: Optional[List[str]] = None


@dataclasses.dataclass
class DecryptResponse:
    """Normalized response from a decryption operation."""
    plaintext: str
    key_id: str
    encryption_algorithm: Optional[str] = None


@dataclasses.dataclass
class EnvelopeEncryptRequest:
    """Request for envelope encryption."""
    plaintext: str
    data_key_spec: str = "AES_256"
    key_id: str = ""
    encryption_context: Optional[Dict[str, str]] = None


@dataclasses.dataclass
class EnvelopeEncryptResponse:
    """Response containing encrypted data key and encrypted payload."""
    encrypted_data_key: str  # base64-encoded
    encrypted_payload: str  # base64-encoded
    plaintext_data_key: Optional[str] = None  # Only available if explicitly requested


@dataclasses.dataclass
class SignRequest:
    """Request for signing a message."""
    message: str
    key_id: str
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256"
    message_type: str = "RAW"


@dataclasses.dataclass
class SignResponse:
    """Response containing the digital signature."""
    signature: str  # base64-encoded
    key_id: str
    signing_algorithm: str


@dataclasses.dataclass
class VerifyRequest:
    """Request for verifying a signature."""
    message: str
    signature: str
    key_id: str
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256"
    message_type: str = "RAW"


@dataclasses.dataclass
class VerifyResponse:
    """Response containing verification result."""
    is_valid: bool
    key_id: str
    signing_algorithm: str


@dataclasses.dataclass
class KeyUsageRecord:
    """Normalized record of a key usage event."""
    event_id: str
    key_id: str
    operation: str
    timestamp: str
    principal: str
    source_ip: Optional[str] = None
    encryption_context: Optional[Dict[str, str]] = None


@dataclasses.dataclass
class KeyUsageSummary:
    """Summary of key usage over a time period."""
    key_id: str
    total_operations: int
    operations_breakdown: Dict[str, int]
    unique_principals: List[str]
    start_time: str
    end_time: str


@dataclasses.dataclass
class CryptoAuditNote:
    """Represents an audit note for embedding and search."""
    note_id: str
    key_id: str
    note_text: str
    severity: str
    created_at: str


@dataclasses.dataclass
class ComplianceNote:
    """Represents a compliance note for translation."""
    note_id: str
    original_text: str
    source_language: str
    target_language: str
    compliance_standard: str = ""


def encode_bytes(value: bytes) -> str:
    """Encode bytes to base64 string."""
    return base64.b64encode(value).decode("utf-8")


def decode_bytes(value: str) -> bytes:
    """Decode base64 string to bytes."""
    return base64.b64decode(value)


def normalize_key_id(raw_key_id: str) -> str:
    """Normalize a key identifier, stripping unnecessary prefixes."""
    if raw_key_id.startswith("arn:"):
        return raw_key_id
    if len(raw_key_id) == 36 and "-" in raw_key_id:
        return raw_key_id
    if raw_key_id.startswith("mrk-"):
        return raw_key_id
    return raw_key_id


def build_encryption_context(**kwargs: str) -> Dict[str, str]:
    """Build a validated encryption context dictionary."""
    context: Dict[str, str] = {}
    for k, v in kwargs.items():
        context[k] = str(v)
    return context


def format_audit_note(note: CryptoAuditNote) -> str:
    """Format an audit note for embedding."""
    return (
        f"[{note.severity.upper()}] Key: {note.key_id} | "
        f"ID: {note.note_id} | {note.note_text}"
    )
