"""
Local helper: security_models.py
Define local request, response, and normalization helpers for Key Management and Encryption.
"""

import base64
import hashlib
import json
import time
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from enum import Enum


class EncryptionAlgorithm(Enum):
    SYMMETRIC_DEFAULT = "SYMMETRIC_DEFAULT"
    RSAES_OAEP_SHA_1 = "RSAES_OAEP_SHA_1"
    RSAES_OAEP_SHA_256 = "RSAES_OAEP_SHA_256"
    SM2PKE = "SM2PKE"


class SigningAlgorithm(Enum):
    RSASSA_PSS_SHA_256 = "RSASSA_PSS_SHA_256"
    RSASSA_PSS_SHA_384 = "RSASSA_PSS_SHA_384"
    RSASSA_PSS_SHA_512 = "RSASSA_PSS_SHA_512"
    RSASSA_PKCS1_V1_5_SHA_256 = "RSASSA_PKCS1_V1_5_SHA_256"
    ECDSA_SHA_256 = "ECDSA_SHA_256"
    ECDSA_SHA_384 = "ECDSA_SHA_384"
    ECDSA_SHA_512 = "ECDSA_SHA_512"


@dataclass
class EncryptRequest:
    """Request model for encryption operations."""

    plaintext: str
    key_id: str
    encryption_algorithm: str = "SYMMETRIC_DEFAULT"
    encryption_context: Optional[Dict[str, str]] = None
    grant_tokens: Optional[List[str]] = None

    def to_provider_params(self) -> Dict[str, Any]:
        """Convert to AWS KMS Encrypt API parameters."""
        params = {
            "KeyId": self.key_id,
            "Plaintext": self.plaintext.encode("utf-8")
            if isinstance(self.plaintext, str)
            else self.plaintext,
            "EncryptionAlgorithm": self.encryption_algorithm,
        }
        if self.encryption_context:
            params["EncryptionContext"] = self.encryption_context
        if self.grant_tokens:
            params["GrantTokens"] = self.grant_tokens
        return params


@dataclass
class DecryptRequest:
    """Request model for decryption operations."""

    ciphertext_blob: bytes
    key_id: Optional[str] = None
    encryption_context: Optional[Dict[str, str]] = None
    grant_tokens: Optional[List[str]] = None

    def to_provider_params(self) -> Dict[str, Any]:
        """Convert to AWS KMS Decrypt API parameters."""
        params = {"CiphertextBlob": self.ciphertext_blob}
        if self.key_id:
            params["KeyId"] = self.key_id
        if self.encryption_context:
            params["EncryptionContext"] = self.encryption_context
        if self.grant_tokens:
            params["GrantTokens"] = self.grant_tokens
        return params


@dataclass
class EnvelopeEncryptionRequest:
    """Request model for envelope encryption."""

    plaintext: str
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None
    data_key_spec: str = "AES_256"

    def to_provider_params(self) -> Dict[str, Any]:
        """Convert to AWS KMS GenerateDataKey API parameters."""
        params = {
            "KeyId": self.key_id,
            "KeySpec": self.data_key_spec,
        }
        if self.encryption_context:
            params["EncryptionContext"] = self.encryption_context
        return params


@dataclass
class SignRequest:
    """Request model for signing operations."""

    message: str
    key_id: str
    signing_algorithm: str = "RSASSA_PSS_SHA_256"
    message_type: str = "RAW"

    def to_provider_params(self) -> Dict[str, Any]:
        """Convert to AWS KMS Sign API parameters."""
        params = {
            "KeyId": self.key_id,
            "Message": self.message.encode("utf-8")
            if isinstance(self.message, str)
            else self.message,
            "SigningAlgorithm": self.signing_algorithm,
            "MessageType": self.message_type,
        }
        return params


@dataclass
class VerifyRequest:
    """Request model for signature verification."""

    message: str
    signature: bytes
    key_id: str
    signing_algorithm: str = "RSASSA_PSS_SHA_256"
    message_type: str = "RAW"

    def to_provider_params(self) -> Dict[str, Any]:
        """Convert to AWS KMS Verify API parameters."""
        params = {
            "KeyId": self.key_id,
            "Message": self.message.encode("utf-8")
            if isinstance(self.message, str)
            else self.message,
            "Signature": self.signature,
            "SigningAlgorithm": self.signing_algorithm,
            "MessageType": self.message_type,
        }
        return params


@dataclass
class EncryptResponse:
    """Response model for encryption operations."""

    success: bool = True
    ciphertext_blob: Optional[str] = None
    key_id: Optional[str] = None
    encryption_algorithm: Optional[str] = None
    request_id: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_provider_response(cls, response: Dict[str, Any]) -> "EncryptResponse":
        ciphertext = response.get("CiphertextBlob")
        return cls(
            success=True,
            ciphertext_blob=base64.b64encode(ciphertext).decode("utf-8")
            if ciphertext
            else None,
            key_id=response.get("KeyId"),
            encryption_algorithm=response.get("EncryptionAlgorithm"),
            request_id=response.get("ResponseMetadata", {}).get("RequestId"),
        )


@dataclass
class DecryptResponse:
    """Response model for decryption operations."""

    success: bool = True
    plaintext: Optional[str] = None
    key_id: Optional[str] = None
    encryption_algorithm: Optional[str] = None
    request_id: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_provider_response(cls, response: Dict[str, Any]) -> "DecryptResponse":
        plaintext_bytes = response.get("Plaintext")
        return cls(
            success=True,
            plaintext=plaintext_bytes.decode("utf-8") if plaintext_bytes else None,
            key_id=response.get("KeyId"),
            encryption_algorithm=response.get("EncryptionAlgorithm"),
            request_id=response.get("ResponseMetadata", {}).get("RequestId"),
        )


@dataclass
class EnvelopeEncryptionResponse:
    """Response model for envelope encryption."""

    success: bool = True
    plaintext_data_key: Optional[bytes] = None
    encrypted_data_key: Optional[str] = None
    key_id: Optional[str] = None
    request_id: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "encrypted_data_key": self.encrypted_data_key,
            "key_id": self.key_id,
            "request_id": self.request_id,
            "error": self.error,
        }

    @classmethod
    def from_provider_response(
        cls, response: Dict[str, Any]
    ) -> "EnvelopeEncryptionResponse":
        encrypted_key = response.get("CiphertextBlob")
        return cls(
            success=True,
            plaintext_data_key=response.get("Plaintext"),
            encrypted_data_key=base64.b64encode(encrypted_key).decode("utf-8")
            if encrypted_key
            else None,
            key_id=response.get("KeyId"),
            request_id=response.get("ResponseMetadata", {}).get("RequestId"),
        )


@dataclass
class SignResponse:
    """Response model for signing operations."""

    success: bool = True
    signature: Optional[str] = None
    key_id: Optional[str] = None
    signing_algorithm: Optional[str] = None
    request_id: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_provider_response(cls, response: Dict[str, Any]) -> "SignResponse":
        signature_bytes = response.get("Signature")
        return cls(
            success=True,
            signature=base64.b64encode(signature_bytes).decode("utf-8")
            if signature_bytes
            else None,
            key_id=response.get("KeyId"),
            signing_algorithm=response.get("SigningAlgorithm"),
            request_id=response.get("ResponseMetadata", {}).get("RequestId"),
        )


@dataclass
class VerifyResponse:
    """Response model for signature verification."""

    success: bool = True
    signature_valid: bool = False
    key_id: Optional[str] = None
    signing_algorithm: Optional[str] = None
    request_id: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_provider_response(cls, response: Dict[str, Any]) -> "VerifyResponse":
        return cls(
            success=True,
            signature_valid=response.get("SignatureValid", False),
            key_id=response.get("KeyId"),
            signing_algorithm=response.get("SigningAlgorithm"),
            request_id=response.get("ResponseMetadata", {}).get("RequestId"),
        )


def normalize_encryption_context(context: Optional[Dict[str, str]]) -> Dict[str, str]:
    """Normalize encryption context for KMS API compatibility."""
    if context is None:
        return {}
    return {str(k): str(v) for k, v in context.items()}


def compute_payload_hash(plaintext: str) -> str:
    """Compute a SHA-256 hash of the plaintext for audit trail."""
    return hashlib.sha256(plaintext.encode("utf-8")).hexdigest()


def create_audit_record(
    operation: str,
    key_id: str,
    request_id: str,
    timestamp: Optional[float] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Create a standardized audit record for crypto operations."""
    record = {
        "operation": operation,
        "key_id": key_id,
        "request_id": request_id,
        "timestamp": timestamp or time.time(),
        "provider": "aws-kms",
        "endpoint": "kms.amazonaws.com",
    }
    if extra:
        record.update(extra)
    return record
