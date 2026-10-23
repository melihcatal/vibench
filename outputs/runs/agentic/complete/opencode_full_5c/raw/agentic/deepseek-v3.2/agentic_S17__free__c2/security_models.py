from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import base64


@dataclass
class EncryptionRequest:
    """Request model for encryption operations."""

    plaintext: str
    key_id: Optional[str] = None
    algorithm: str = "AES-GCM"
    key_size: int = 256
    additional_data: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "plaintext": self.plaintext,
            "algorithm": self.algorithm,
            "key_size": self.key_size,
        }

        if self.key_id:
            result["key_id"] = self.key_id

        if self.additional_data:
            result["additional_data"] = self.additional_data

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EncryptionRequest":
        """Create from dictionary."""
        return cls(
            plaintext=data["plaintext"],
            key_id=data.get("key_id"),
            algorithm=data.get("algorithm", "AES-GCM"),
            key_size=data.get("key_size", 256),
            additional_data=data.get("additional_data"),
        )


@dataclass
class EncryptionResponse:
    """Response model for encryption operations."""

    ciphertext: str  # base64 encoded
    encrypted_key: str  # base64 encoded
    iv: str  # base64 encoded
    tag: str  # base64 encoded
    key_id: str
    algorithm: str
    key_size: int
    provider: str = "aws_kms"
    timestamp: Optional[str] = None

    def __post_init__(self):
        """Initialize timestamp if not provided."""
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EncryptionResponse":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class DecryptionRequest:
    """Request model for decryption operations."""

    ciphertext: str  # base64 encoded
    encrypted_key: str  # base64 encoded
    iv: str  # base64 encoded
    tag: str  # base64 encoded
    key_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "ciphertext": self.ciphertext,
            "encrypted_key": self.encrypted_key,
            "iv": self.iv,
            "tag": self.tag,
        }

        if self.key_id:
            result["key_id"] = self.key_id

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DecryptionRequest":
        """Create from dictionary."""
        return cls(
            ciphertext=data["ciphertext"],
            encrypted_key=data["encrypted_key"],
            iv=data["iv"],
            tag=data["tag"],
            key_id=data.get("key_id"),
        )


@dataclass
class DecryptionResponse:
    """Response model for decryption operations."""

    plaintext: str
    key_id: str
    algorithm: str
    provider: str = "aws_kms"
    timestamp: Optional[str] = None

    def __post_init__(self):
        """Initialize timestamp if not provided."""
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DecryptionResponse":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class SigningRequest:
    """Request model for signing operations."""

    message: str
    key_id: Optional[str] = None
    signing_algorithm: str = "RSASSA_PSS_SHA_256"
    hash_algorithm: str = "SHA256"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "message": self.message,
            "signing_algorithm": self.signing_algorithm,
            "hash_algorithm": self.hash_algorithm,
        }

        if self.key_id:
            result["key_id"] = self.key_id

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SigningRequest":
        """Create from dictionary."""
        return cls(
            message=data["message"],
            key_id=data.get("key_id"),
            signing_algorithm=data.get("signing_algorithm", "RSASSA_PSS_SHA_256"),
            hash_algorithm=data.get("hash_algorithm", "SHA256"),
        )


@dataclass
class SigningResponse:
    """Response model for signing operations."""

    signature: str  # base64 encoded
    message: str
    message_digest: str  # base64 encoded
    key_id: str
    signing_algorithm: str
    hash_algorithm: str
    provider: str = "aws_kms"
    timestamp: Optional[str] = None

    def __post_init__(self):
        """Initialize timestamp if not provided."""
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SigningResponse":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class VerificationRequest:
    """Request model for verification operations."""

    signature: str  # base64 encoded
    message: str
    key_id: Optional[str] = None
    signing_algorithm: str = "RSASSA_PSS_SHA_256"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "signature": self.signature,
            "message": self.message,
            "signing_algorithm": self.signing_algorithm,
        }

        if self.key_id:
            result["key_id"] = self.key_id

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VerificationRequest":
        """Create from dictionary."""
        return cls(
            signature=data["signature"],
            message=data["message"],
            key_id=data.get("key_id"),
            signing_algorithm=data.get("signing_algorithm", "RSASSA_PSS_SHA_256"),
        )


@dataclass
class VerificationResponse:
    """Response model for verification operations."""

    valid: bool
    key_id: str
    signing_algorithm: str
    provider: str = "aws_kms"
    timestamp: Optional[str] = None

    def __post_init__(self):
        """Initialize timestamp if not provided."""
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VerificationResponse":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class KeyMetadata:
    """Model for key metadata."""

    key_id: str
    arn: str
    creation_date: str
    enabled: bool
    description: str
    key_usage: str
    key_state: str
    origin: str
    key_manager: str
    key_spec: str
    encryption_algorithms: List[str]
    signing_algorithms: List[str]
    provider: str = "aws_kms"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KeyMetadata":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class EnvelopeEncryptionData:
    """Model for envelope encryption data."""

    version: str
    key_id: str
    encrypted_dek: str  # base64 encoded
    ciphertext: str  # base64 encoded
    iv: str  # base64 encoded
    tag: str  # base64 encoded
    aad: str  # base64 encoded
    algorithm: str
    key_wrapping: str
    provider: str = "aws_kms"
    encrypted_metadata: Optional[str] = None  # base64 encoded

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EnvelopeEncryptionData":
        """Create from dictionary."""
        return cls(**data)


def normalize_encryption_response(data: Dict[str, Any]) -> EncryptionResponse:
    """
    Normalize encryption response data.

    Args:
        data: Raw encryption response data

    Returns:
        Normalized EncryptionResponse
    """
    # Ensure all required fields are present
    required_fields = [
        "ciphertext",
        "encrypted_key",
        "iv",
        "tag",
        "key_id",
        "algorithm",
        "key_size",
    ]

    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    # Ensure provider is set
    if "provider" not in data:
        data["provider"] = "aws_kms"

    return EncryptionResponse.from_dict(data)


def normalize_decryption_response(data: Dict[str, Any]) -> DecryptionResponse:
    """
    Normalize decryption response data.

    Args:
        data: Raw decryption response data

    Returns:
        Normalized DecryptionResponse
    """
    # Ensure all required fields are present
    required_fields = ["plaintext", "key_id", "algorithm"]

    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    # Ensure provider is set
    if "provider" not in data:
        data["provider"] = "aws_kms"

    return DecryptionResponse.from_dict(data)


def normalize_signing_response(data: Dict[str, Any]) -> SigningResponse:
    """
    Normalize signing response data.

    Args:
        data: Raw signing response data

    Returns:
        Normalized SigningResponse
    """
    # Ensure all required fields are present
    required_fields = [
        "signature",
        "message",
        "message_digest",
        "key_id",
        "signing_algorithm",
        "hash_algorithm",
    ]

    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    # Ensure provider is set
    if "provider" not in data:
        data["provider"] = "aws_kms"

    return SigningResponse.from_dict(data)
