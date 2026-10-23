from typing import Optional, Any, Dict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EncryptionRequest:
    """Request model for encryption operations."""

    plaintext: str
    key_id: str
    context: Optional[Dict[str, str]] = None


@dataclass
class EncryptionResponse:
    """Response model for encryption operations."""

    success: bool
    ciphertext: Optional[bytes] = None
    key_id: Optional[str] = None
    algorithm: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class DecryptionRequest:
    """Request model for decryption operations."""

    ciphertext: bytes
    key_id: str
    context: Optional[Dict[str, str]] = None


@dataclass
class DecryptionResponse:
    """Response model for decryption operations."""

    success: bool
    plaintext: Optional[str] = None
    key_id: Optional[str] = None
    algorithm: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class EnvelopeEncryptionRequest:
    """Request model for envelope encryption."""

    plaintext: str
    key_id: str
    context: Optional[Dict[str, str]] = None


@dataclass
class EnvelopeEncryptionResponse:
    """Response model for envelope encryption."""

    success: bool
    ciphertext: Optional[bytes] = None
    encrypted_dek: Optional[bytes] = None
    iv: Optional[bytes] = None
    key_id: Optional[str] = None
    algorithm: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class SignRequest:
    """Request model for signing operations."""

    data: bytes
    key_id: str
    algorithm: Optional[str] = None


@dataclass
class SignResponse:
    """Response model for signing operations."""

    success: bool
    signature: Optional[bytes] = None
    key_id: Optional[str] = None
    algorithm: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class VerifyRequest:
    """Request model for verification operations."""

    data: bytes
    signature: bytes
    key_id: str
    algorithm: Optional[str] = None


@dataclass
class VerifyResponse:
    """Response model for verification operations."""

    success: bool
    is_valid: Optional[bool] = None
    key_id: Optional[str] = None
    algorithm: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class KeyUsageEvent:
    """Model for tracking key usage events."""

    event_id: str
    key_id: str
    operation: str
    timestamp: datetime
    success: bool
    data_size: Optional[int] = None
    algorithm: Optional[str] = None
    provider: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class CryptoAuditNote:
    """Model for crypto audit notes."""

    note_id: str
    timestamp: datetime
    operation: str
    key_id: str
    note_text: str
    severity: str = "info"  # info, warning, error
    tags: Optional[list] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
