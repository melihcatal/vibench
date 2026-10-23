from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class EncryptionRequest:
    """Request model for encryption operations."""

    plaintext: str
    key_id: Optional[str] = None
    algorithm: Optional[str] = None
    context: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def validate(self) -> List[str]:
        """Validate request fields."""
        errors = []
        if not self.plaintext or not isinstance(self.plaintext, str):
            errors.append("plaintext must be a non-empty string")
        if self.context and not isinstance(self.context, dict):
            errors.append("context must be a dictionary")
        return errors


@dataclass
class EncryptionResponse:
    """Response model for encryption operations."""

    ciphertext: str
    key_id: str
    algorithm: str
    provider: str = "aws_kms"
    timestamp: str = ""
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        if self.metadata:
            result["metadata"] = self.metadata
        return result


@dataclass
class EnvelopeEncryptionRequest:
    """Request model for envelope encryption."""

    plaintext: str
    key_id: Optional[str] = None
    key_spec: str = "AES_256"
    encryption_mode: str = "AES-GCM"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def validate(self) -> List[str]:
        """Validate request fields."""
        errors = []
        if not self.plaintext or not isinstance(self.plaintext, str):
            errors.append("plaintext must be a non-empty string")
        if self.key_spec not in ["AES_128", "AES_256"]:
            errors.append("key_spec must be AES_128 or AES_256")
        return errors


@dataclass
class EnvelopeEncryptionResponse:
    """Response model for envelope encryption."""

    encrypted_data: str
    encrypted_dek: str
    iv: str
    tag: str
    key_id: str
    algorithm: str
    provider: str = "aws_kms"
    timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class DecryptionRequest:
    """Request model for decryption operations."""

    ciphertext: str
    key_id: Optional[str] = None
    algorithm: Optional[str] = None
    context: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def validate(self) -> List[str]:
        """Validate request fields."""
        errors = []
        if not self.ciphertext or not isinstance(self.ciphertext, str):
            errors.append("ciphertext must be a non-empty string")
        if self.context and not isinstance(self.context, dict):
            errors.append("context must be a dictionary")
        return errors


@dataclass
class DecryptionResponse:
    """Response model for decryption operations."""

    plaintext: str
    key_id: str
    algorithm: str
    provider: str = "aws_kms"
    timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class SigningRequest:
    """Request model for signing operations."""

    message: str
    key_id: Optional[str] = None
    algorithm: str = "RSASSA_PSS_SHA_256"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def validate(self) -> List[str]:
        """Validate request fields."""
        errors = []
        if not self.message or not isinstance(self.message, str):
            errors.append("message must be a non-empty string")
        if self.algorithm not in [
            "RSASSA_PSS_SHA_256",
            "RSASSA_PSS_SHA_384",
            "RSASSA_PSS_SHA_512",
        ]:
            errors.append("algorithm must be a valid RSA signing algorithm")
        return errors


@dataclass
class SigningResponse:
    """Response model for signing operations."""

    signature: str
    key_id: str
    algorithm: str
    message_digest: str
    provider: str = "aws_kms"
    timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class VerificationRequest:
    """Request model for verification operations."""

    message: str
    signature: str
    key_id: Optional[str] = None
    algorithm: str = "RSASSA_PSS_SHA_256"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def validate(self) -> List[str]:
        """Validate request fields."""
        errors = []
        if not self.message or not isinstance(self.message, str):
            errors.append("message must be a non-empty string")
        if not self.signature or not isinstance(self.signature, str):
            errors.append("signature must be a non-empty string")
        return errors


@dataclass
class VerificationResponse:
    """Response model for verification operations."""

    valid: bool
    key_id: str
    algorithm: str
    provider: str = "aws_kms"
    timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class KeyMetadata:
    """Model for key metadata."""

    key_id: str
    arn: str
    creation_date: str
    description: str
    key_state: str
    key_usage: str
    key_spec: str
    origin: str
    provider: str = "aws_kms"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class CryptoEvent:
    """Model for cryptographic operation events."""

    operation: str  # 'encrypt', 'decrypt', 'sign', 'verify'
    key_id: str
    algorithm: str
    timestamp: str
    success: bool
    error_message: Optional[str] = None
    payload_size: Optional[int] = None
    provider: str = "aws_kms"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


def normalize_timestamp(timestamp: Optional[str] = None) -> str:
    """Normalize timestamp to ISO format."""
    if timestamp:
        return timestamp
    return datetime.utcnow().isoformat() + "Z"


def serialize_for_storage(data: Any) -> str:
    """Serialize data for storage."""
    if isinstance(data, (dict, list)):
        return json.dumps(data, sort_keys=True)
    return str(data)


def deserialize_from_storage(data: str) -> Any:
    """Deserialize data from storage."""
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return data
