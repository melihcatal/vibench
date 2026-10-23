from typing import Dict, Any, Optional, Union, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import base64


@dataclass
class EncryptionRequest:
    """Request model for encryption operations."""

    plaintext: Union[str, bytes]
    key_id: Optional[str] = None
    encryption_context: Optional[Dict[str, str]] = None
    key_spec: Optional[str] = "SYMMETRIC_DEFAULT"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API calls."""
        result = {
            "plaintext": self.plaintext
            if isinstance(self.plaintext, bytes)
            else self.plaintext.encode("utf-8")
        }
        if self.key_id:
            result["key_id"] = self.key_id
        if self.encryption_context:
            result["encryption_context"] = self.encryption_context
        if self.key_spec:
            result["key_spec"] = self.key_spec
        return result


@dataclass
class EncryptionResponse:
    """Response model for encryption operations."""

    ciphertext: str  # Base64-encoded
    key_id: str
    encryption_context: Dict[str, str]
    provider: str = "aws_kms"
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


@dataclass
class DecryptionRequest:
    """Request model for decryption operations."""

    ciphertext: Union[str, bytes]  # Base64-encoded string or bytes
    key_id: Optional[str] = None
    encryption_context: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API calls."""
        result = {
            "ciphertext": self.ciphertext
            if isinstance(self.ciphertext, bytes)
            else base64.b64decode(self.ciphertext)
        }
        if self.key_id:
            result["key_id"] = self.key_id
        if self.encryption_context:
            result["encryption_context"] = self.encryption_context
        return result


@dataclass
class DecryptionResponse:
    """Response model for decryption operations."""

    plaintext: bytes
    plaintext_str: Optional[str] = None
    key_id: str
    encryption_context: Dict[str, str]
    provider: str = "aws_kms"
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()
        if self.plaintext_str is None:
            try:
                self.plaintext_str = self.plaintext.decode("utf-8")
            except UnicodeDecodeError:
                self.plaintext_str = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class EnvelopeEncryptionRequest:
    """Request model for envelope encryption."""

    plaintext: Union[str, bytes]
    key_id: Optional[str] = None
    encryption_context: Optional[Dict[str, str]] = None
    key_spec: Optional[str] = "AES_256"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "plaintext": self.plaintext
            if isinstance(self.plaintext, bytes)
            else self.plaintext.encode("utf-8")
        }
        if self.key_id:
            result["key_id"] = self.key_id
        if self.encryption_context:
            result["encryption_context"] = self.encryption_context
        if self.key_spec:
            result["key_spec"] = self.key_spec
        return result


@dataclass
class EnvelopeEncryptionResponse:
    """Response model for envelope encryption."""

    ciphertext: str  # Base64-encoded
    encrypted_data_key: str  # Base64-encoded
    nonce: str  # Base64-encoded
    key_id: str
    encryption_context: Dict[str, str]
    provider: str = "aws_kms"
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class SigningRequest:
    """Request model for signing operations."""

    message: Union[str, bytes]
    key_id: Optional[str] = None
    signing_algorithm: Optional[str] = "RSASSA_PSS_SHA_256"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "message": self.message
            if isinstance(self.message, bytes)
            else self.message.encode("utf-8")
        }
        if self.key_id:
            result["key_id"] = self.key_id
        if self.signing_algorithm:
            result["signing_algorithm"] = self.signing_algorithm
        return result


@dataclass
class SigningResponse:
    """Response model for signing operations."""

    signature: str  # Base64-encoded
    message_digest: str  # Base64-encoded
    key_id: str
    signing_algorithm: str
    provider: str = "aws_kms"
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class VerificationResponse:
    """Response model for signature verification."""

    signature_valid: bool
    key_id: str
    signing_algorithm: str
    provider: str = "aws_kms"
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

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


def normalize_payload(payload: Any) -> bytes:
    """Normalize any payload to bytes for encryption."""
    if isinstance(payload, bytes):
        return payload
    elif isinstance(payload, str):
        return payload.encode("utf-8")
    elif isinstance(payload, (dict, list)):
        return json.dumps(payload).encode("utf-8")
    else:
        return str(payload).encode("utf-8")


def parse_encryption_result(result: Dict[str, Any]) -> EncryptionResponse:
    """Parse AWS KMS encryption result to standardized response."""
    return EncryptionResponse(
        ciphertext=base64.b64encode(result["CiphertextBlob"]).decode("utf-8"),
        key_id=result.get("KeyId", ""),
        encryption_context=result.get("EncryptionContext", {}),
        provider="aws_kms",
    )


def parse_decryption_result(result: Dict[str, Any]) -> DecryptionResponse:
    """Parse AWS KMS decryption result to standardized response."""
    return DecryptionResponse(
        plaintext=result["Plaintext"],
        key_id=result.get("KeyId", ""),
        encryption_context=result.get("EncryptionContext", {}),
        provider="aws_kms",
    )
