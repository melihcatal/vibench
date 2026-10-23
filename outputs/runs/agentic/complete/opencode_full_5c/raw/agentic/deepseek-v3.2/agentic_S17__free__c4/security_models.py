from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Union, List
from enum import Enum
import json
import base64
from datetime import datetime


class EncryptionAlgorithm(str, Enum):
    """Supported encryption algorithms."""

    AES_GCM_256 = "AES-GCM-256"
    AES_CBC_256 = "AES-CBC-256"
    RSA_OAEP_2048 = "RSA-OAEP-2048"
    RSA_OAEP_4096 = "RSA-OAEP-4096"


class SigningAlgorithm(str, Enum):
    """Supported signing algorithms."""

    RSASSA_PKCS1_V1_5_SHA_256 = "RSASSA_PKCS1_V1_5_SHA_256"
    RSASSA_PKCS1_V1_5_SHA_512 = "RSASSA_PKCS1_V1_5_SHA_512"
    RSASSA_PSS_SHA_256 = "RSASSA_PSS_SHA_256"
    RSASSA_PSS_SHA_512 = "RSASSA_PSS_SHA_512"
    ECDSA_SHA_256 = "ECDSA_SHA_256"
    ECDSA_SHA_512 = "ECDSA_SHA_512"


class SecurityProvider(str, Enum):
    """Supported security providers."""

    AWS_KMS = "aws_kms"
    GCP_KMS = "gcp_kms"
    AZURE_KEYVAULT = "azure_keyvault"


class KeyType(str, Enum):
    """Key types."""

    SYMMETRIC = "symmetric"
    ASYMMETRIC = "asymmetric"
    HMAC = "hmac"


@dataclass
class EncryptionRequest:
    """Request model for encryption operations."""

    plaintext: Union[str, bytes, Dict]
    key_id: Optional[str] = None
    provider: SecurityProvider = SecurityProvider.AWS_KMS
    algorithm: EncryptionAlgorithm = EncryptionAlgorithm.AES_GCM_256
    context: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        result = {
            "provider": self.provider.value,
            "algorithm": self.algorithm.value,
            "context": self.context,
        }

        if self.key_id:
            result["key_id"] = self.key_id

        # Handle plaintext
        if isinstance(self.plaintext, str):
            result["plaintext"] = self.plaintext
        elif isinstance(self.plaintext, bytes):
            result["plaintext"] = base64.b64encode(self.plaintext).decode("utf-8")
        elif isinstance(self.plaintext, dict):
            result["plaintext"] = json.dumps(self.plaintext)
        else:
            result["plaintext"] = str(self.plaintext)

        return result

    @classmethod
    def from_dict(cls, data: Dict) -> "EncryptionRequest":
        """Create from dictionary."""
        # Handle plaintext
        plaintext = data.get("plaintext", "")
        if isinstance(plaintext, str):
            # Check if it's base64 encoded
            try:
                decoded = base64.b64decode(plaintext)
                plaintext = decoded
            except:
                pass

        return cls(
            plaintext=plaintext,
            key_id=data.get("key_id"),
            provider=SecurityProvider(
                data.get("provider", SecurityProvider.AWS_KMS.value)
            ),
            algorithm=EncryptionAlgorithm(
                data.get("algorithm", EncryptionAlgorithm.AES_GCM_256.value)
            ),
            context=data.get("context", {}),
        )


@dataclass
class EncryptionResult:
    """Result model for encryption operations."""

    ciphertext: str
    provider: SecurityProvider
    algorithm: EncryptionAlgorithm
    key_id: Optional[str] = None
    encrypted_key: Optional[str] = None
    iv: Optional[str] = None
    tag: Optional[str] = None
    context: Dict[str, str] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    version: str = "1.0"
    envelope_encryption: bool = False

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        result = {
            "ciphertext": self.ciphertext,
            "provider": self.provider.value,
            "algorithm": self.algorithm.value,
            "timestamp": self.timestamp,
            "version": self.version,
            "envelope_encryption": self.envelope_encryption,
            "context": self.context,
        }

        if self.key_id:
            result["key_id"] = self.key_id
        if self.encrypted_key:
            result["encrypted_key"] = self.encrypted_key
        if self.iv:
            result["iv"] = self.iv
        if self.tag:
            result["tag"] = self.tag

        return result

    @classmethod
    def from_dict(cls, data: Dict) -> "EncryptionResult":
        """Create from dictionary."""
        return cls(
            ciphertext=data["ciphertext"],
            provider=SecurityProvider(data["provider"]),
            algorithm=EncryptionAlgorithm(
                data.get("algorithm", EncryptionAlgorithm.AES_GCM_256.value)
            ),
            key_id=data.get("key_id"),
            encrypted_key=data.get("encrypted_key"),
            iv=data.get("iv"),
            tag=data.get("tag"),
            context=data.get("context", {}),
            timestamp=data.get("timestamp", datetime.utcnow().isoformat() + "Z"),
            version=data.get("version", "1.0"),
            envelope_encryption=data.get("envelope_encryption", False),
        )


@dataclass
class DecryptionRequest:
    """Request model for decryption operations."""

    encryption_result: Union[EncryptionResult, Dict]
    provider: Optional[SecurityProvider] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        if isinstance(self.encryption_result, EncryptionResult):
            result = self.encryption_result.to_dict()
        else:
            result = self.encryption_result

        if self.provider:
            result["provider"] = self.provider.value

        return result


@dataclass
class SigningRequest:
    """Request model for signing operations."""

    data: Union[str, bytes, Dict]
    key_id: Optional[str] = None
    provider: SecurityProvider = SecurityProvider.AWS_KMS
    algorithm: SigningAlgorithm = SigningAlgorithm.RSASSA_PKCS1_V1_5_SHA_256
    message_type: str = "DIGEST"

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        result = {
            "provider": self.provider.value,
            "algorithm": self.algorithm.value,
            "message_type": self.message_type,
        }

        if self.key_id:
            result["key_id"] = self.key_id

        # Handle data
        if isinstance(self.data, str):
            result["data"] = self.data
        elif isinstance(self.data, bytes):
            result["data"] = base64.b64encode(self.data).decode("utf-8")
        elif isinstance(self.data, dict):
            result["data"] = json.dumps(self.data)
        else:
            result["data"] = str(self.data)

        return result


@dataclass
class SignatureResult:
    """Result model for signing operations."""

    signature: str
    provider: SecurityProvider
    algorithm: SigningAlgorithm
    key_id: str
    data_hash: Optional[str] = None
    message_type: str = "DIGEST"
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    verified: bool = False

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        result = {
            "signature": self.signature,
            "provider": self.provider.value,
            "algorithm": self.algorithm.value,
            "key_id": self.key_id,
            "message_type": self.message_type,
            "timestamp": self.timestamp,
            "verified": self.verified,
        }

        if self.data_hash:
            result["data_hash"] = self.data_hash

        return result


@dataclass
class KeyMetadata:
    """Metadata for managed keys."""

    key_id: str
    provider: SecurityProvider
    key_type: KeyType
    algorithm: Union[EncryptionAlgorithm, SigningAlgorithm]
    created_at: str
    enabled: bool = True
    description: Optional[str] = None
    rotation_enabled: bool = False
    rotation_period: Optional[int] = None
    tags: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "key_id": self.key_id,
            "provider": self.provider.value,
            "key_type": self.key_type.value,
            "algorithm": self.algorithm.value,
            "created_at": self.created_at,
            "enabled": self.enabled,
            "description": self.description,
            "rotation_enabled": self.rotation_enabled,
            "rotation_period": self.rotation_period,
            "tags": self.tags,
        }


@dataclass
class CryptoEvent:
    """Model for cryptographic events."""

    event_id: str
    operation: str  # encrypt, decrypt, sign, verify, etc.
    key_id: str
    provider: SecurityProvider
    timestamp: str
    success: bool
    data_size: Optional[int] = None
    algorithm: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        result = {
            "event_id": self.event_id,
            "operation": self.operation,
            "key_id": self.key_id,
            "provider": self.provider.value,
            "timestamp": self.timestamp,
            "success": self.success,
            "metadata": self.metadata,
        }

        if self.data_size:
            result["data_size"] = self.data_size
        if self.algorithm:
            result["algorithm"] = self.algorithm
        if self.error_message:
            result["error_message"] = self.error_message

        return result


@dataclass
class EnvelopeEncryptionResult:
    """Result model for envelope encryption."""

    encrypted_data: str
    encrypted_dek: str
    data_hash: str
    provider: SecurityProvider
    key_id: str
    algorithm: EncryptionAlgorithm = EncryptionAlgorithm.AES_GCM_256
    iv: Optional[str] = None
    tag: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        result = {
            "encrypted_data": self.encrypted_data,
            "encrypted_dek": self.encrypted_dek,
            "data_hash": self.data_hash,
            "provider": self.provider.value,
            "key_id": self.key_id,
            "algorithm": self.algorithm.value,
            "timestamp": self.timestamp,
        }

        if self.iv:
            result["iv"] = self.iv
        if self.tag:
            result["tag"] = self.tag

        return result


def normalize_encryption_result(result: Dict) -> EncryptionResult:
    """Normalize encryption result from various providers."""
    # Check if it's already an EncryptionResult
    if isinstance(result, EncryptionResult):
        return result

    # Extract provider
    provider_str = result.get("provider", "aws_kms")
    if provider_str == "aws":
        provider_str = "aws_kms"
    elif provider_str == "gcp":
        provider_str = "gcp_kms"
    elif provider_str == "azure":
        provider_str = "azure_keyvault"

    # Extract algorithm
    algorithm_str = result.get("algorithm", "AES-GCM-256")

    return EncryptionResult(
        ciphertext=result["ciphertext"],
        provider=SecurityProvider(provider_str),
        algorithm=EncryptionAlgorithm(algorithm_str),
        key_id=result.get("key_id"),
        encrypted_key=result.get("encrypted_key"),
        iv=result.get("iv"),
        tag=result.get("tag"),
        context=result.get("context", {}),
        timestamp=result.get("timestamp", datetime.utcnow().isoformat() + "Z"),
        version=result.get("version", "1.0"),
        envelope_encryption=result.get("envelope_encryption", False),
    )


def normalize_signature_result(result: Dict) -> SignatureResult:
    """Normalize signature result from various providers."""
    # Extract provider
    provider_str = result.get("provider", "aws_kms")
    if provider_str == "aws":
        provider_str = "aws_kms"
    elif provider_str == "azure":
        provider_str = "azure_keyvault"

    # Extract algorithm
    algorithm_str = result.get("algorithm", "RSASSA_PKCS1_V1_5_SHA_256")

    return SignatureResult(
        signature=result["signature"],
        provider=SecurityProvider(provider_str),
        algorithm=SigningAlgorithm(algorithm_str),
        key_id=result.get("key_id", ""),
        data_hash=result.get("data_hash"),
        message_type=result.get("message_type", "DIGEST"),
        timestamp=result.get("timestamp", datetime.utcnow().isoformat() + "Z"),
        verified=result.get("verified", False),
    )
