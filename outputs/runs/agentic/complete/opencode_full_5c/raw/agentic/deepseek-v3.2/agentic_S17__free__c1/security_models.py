from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class EncryptionRequest:
    """Request model for encryption operations."""

    plaintext: str
    key_name: Optional[str] = None
    context: Optional[Dict[str, str]] = None
    algorithm: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EncryptionRequest":
        return cls(**data)


@dataclass
class EncryptionResponse:
    """Response model for encryption operations."""

    ciphertext: str
    key_name: str
    algorithm: str
    provider: str
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EncryptionResponse":
        return cls(**data)


@dataclass
class DecryptionRequest:
    """Request model for decryption operations."""

    ciphertext: str
    key_name: str
    context: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DecryptionRequest":
        return cls(**data)


@dataclass
class DecryptionResponse:
    """Response model for decryption operations."""

    plaintext: str
    key_name: str
    algorithm: str
    provider: str
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DecryptionResponse":
        return cls(**data)


@dataclass
class EnvelopeEncryptionRequest:
    """Request model for envelope encryption."""

    plaintext: str
    key_name: str
    dek_algorithm: str = "AES-256-CBC"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EnvelopeEncryptionRequest":
        return cls(**data)


@dataclass
class EnvelopeEncryptionResponse:
    """Response model for envelope encryption."""

    ciphertext: str
    encrypted_dek: str
    iv: str
    key_name: str
    algorithm: str
    provider: str
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EnvelopeEncryptionResponse":
        return cls(**data)


@dataclass
class SigningRequest:
    """Request model for signing operations."""

    data: str
    key_name: str
    hash_algorithm: str = "SHA256"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SigningRequest":
        return cls(**data)


@dataclass
class SigningResponse:
    """Response model for signing operations."""

    signature: str
    key_name: str
    data_hash: str
    algorithm: str
    provider: str
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SigningResponse":
        return cls(**data)


@dataclass
class VerificationRequest:
    """Request model for verification operations."""

    data: str
    signature: str
    key_name: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VerificationRequest":
        return cls(**data)


@dataclass
class VerificationResponse:
    """Response model for verification operations."""

    is_valid: bool
    key_name: str
    algorithm: str
    provider: str
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VerificationResponse":
        return cls(**data)


@dataclass
class CryptoEvent:
    """Model for cryptographic operation events."""

    operation: str
    key_name: str
    provider: str
    timestamp: str
    success: bool
    data_size: Optional[int] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CryptoEvent":
        return cls(**data)
