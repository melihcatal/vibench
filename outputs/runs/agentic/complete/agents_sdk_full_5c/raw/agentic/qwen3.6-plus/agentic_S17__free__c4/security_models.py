"""
Local request, response, and normalization helpers for Key Management and Encryption.
Provides data models, payload normalization, and response parsing utilities.
"""

import base64
import json
import time
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List


@dataclass
class EncryptionRequest:
    """Request model for encryption operations."""
    plaintext: str = ""
    key_id: str = ""
    encryption_context: Optional[Dict[str, str]] = field(default_factory=dict)
    algorithm: str = "SYMMETRIC_DEFAULT"
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)

    def to_normalized_payload(self) -> bytes:
        """Normalize plaintext to bytes for encryption."""
        if isinstance(self.plaintext, str):
            return self.plaintext.encode("utf-8")
        return self.plaintext


@dataclass
class EncryptionResponse:
    """Response model for encryption operations."""
    ciphertext: str = ""
    key_id: str = ""
    algorithm: str = ""
    encryption_context: Optional[Dict[str, str]] = field(default_factory=dict)
    request_id: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EncryptionResponse":
        return cls(**data)


@dataclass
class DecryptionRequest:
    """Request model for decryption operations."""
    ciphertext: str = ""
    encryption_context: Optional[Dict[str, str]] = field(default_factory=dict)
    algorithm: Optional[str] = None

    def get_ciphertext_bytes(self) -> bytes:
        """Decode ciphertext from base64 or raw bytes."""
        try:
            return base64.b64decode(self.ciphertext)
        except Exception:
            return self.ciphertext.encode("utf-8") if isinstance(self.ciphertext, str) else self.ciphertext


@dataclass
class DecryptionResponse:
    """Response model for decryption operations."""
    plaintext: str = ""
    key_id: str = ""
    encryption_context: Optional[Dict[str, str]] = field(default_factory=dict)
    request_id: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class SigningRequest:
    """Request model for signing operations."""
    message: str = ""
    key_id: str = ""
    message_type: str = "RAW"
    algorithm: str = "RSASSA_PSS_SHA_256"

    def get_message_bytes(self) -> bytes:
        return self.message.encode("utf-8")


@dataclass
class SigningResponse:
    """Response model for signing operations."""
    signature: str = ""
    key_id: str = ""
    algorithm: str = ""
    request_id: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def get_signature_bytes(self) -> bytes:
        return base64.b64decode(self.signature)


@dataclass
class VerificationRequest:
    """Request model for signature verification."""
    message: str = ""
    signature: str = ""
    key_id: str = ""
    message_type: str = "RAW"
    algorithm: str = "RSASSA_PSS_SHA_256"

    def get_message_bytes(self) -> bytes:
        return self.message.encode("utf-8")

    def get_signature_bytes(self) -> bytes:
        return base64.b64decode(self.signature)


@dataclass
class VerificationResponse:
    """Response model for signature verification."""
    is_valid: bool = False
    key_id: str = ""
    request_id: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EnvelopeEncryptionRequest:
    """Request model for envelope encryption."""
    plaintext: str = ""
    key_id: str = ""
    encryption_context: Optional[Dict[str, str]] = field(default_factory=dict)
    data_key_length: int = 32

    def to_normalized_payload(self) -> bytes:
        if isinstance(self.plaintext, str):
            return self.plaintext.encode("utf-8")
        return self.plaintext


@dataclass
class EnvelopeEncryptionResponse:
    """Response model for envelope encryption."""
    encrypted_data_key: str = ""
    encrypted_payload: str = ""
    key_id: str = ""
    encryption_context: Optional[Dict[str, str]] = field(default_factory=dict)
    algorithm: str = ""
    request_id: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class KeyUsageEvent:
    """Model for a single key usage event."""
    key_id: str = ""
    action: str = ""
    timestamp: float = 0.0
    status: str = "SUCCESS"
    error_code: Optional[str] = None
    encryption_context: Optional[Dict[str, str]] = None
    request_id: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class KeyUsageSummary:
    """Summary of key usage events."""
    key_id: str = ""
    total_operations: int = 0
    encrypt_count: int = 0
    decrypt_count: int = 0
    sign_count: int = 0
    verify_count: int = 0
    generate_data_key_count: int = 0
    error_count: int = 0
    events: List[KeyUsageEvent] = field(default_factory=list)
    period_start: float = 0.0
    period_end: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["events"] = [e.to_dict() for e in self.events]
        return result

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class SafetyCheckRequest:
    """Request model for payload safety checks."""
    text: str = ""
    attributes: Optional[List[str]] = field(default_factory=list)

    def to_normalized_text(self) -> str:
        return self.text.strip()


@dataclass
class SafetyCheckResponse:
    """Response model for payload safety checks."""
    is_safe: bool = True
    attributes: Dict[str, float] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EmbeddingRequest:
    """Request model for text embeddings."""
    text: str = ""
    model: str = "text-embedding-3-small"
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)

    def to_normalized_text(self) -> str:
        return self.text.strip()


@dataclass
class EmbeddingResponse:
    """Response model for embeddings."""
    embedding: List[float] = field(default_factory=list)
    model: str = ""
    text: str = ""
    timestamp: float = field(default_factory=time.time)
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class TranslationRequest:
    """Request model for translation operations."""
    text: str = ""
    source_language: str = "en"
    target_language: str = "es"

    def to_normalized_text(self) -> str:
        return self.text.strip()


@dataclass
class TranslationResponse:
    """Response model for translation operations."""
    translated_text: str = ""
    source_language: str = ""
    target_language: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def normalize_encryption_context(context: Optional[Dict[str, str]]) -> Dict[str, str]:
    """Normalize encryption context to string-string mapping."""
    if context is None:
        return {}
    return {str(k): str(v) for k, v in context.items()}


def encode_ciphertext(ciphertext_bytes: bytes) -> str:
    """Encode ciphertext bytes to base64 string."""
    return base64.b64encode(ciphertext_bytes).decode("utf-8")


def decode_ciphertext(ciphertext_str: str) -> bytes:
    """Decode base64 ciphertext string to bytes."""
    return base64.b64decode(ciphertext_str)


def parse_aws_kms_encrypt_response(response: Dict[str, Any]) -> EncryptionResponse:
    """Parse AWS KMS encrypt API response into EncryptionResponse model."""
    return EncryptionResponse(
        ciphertext=encode_ciphertext(response.get("CiphertextBlob", b"")),
        key_id=response.get("KeyId", ""),
        algorithm=response.get("EncryptionAlgorithm", ""),
        encryption_context=response.get("EncryptionContext", {}),
        request_id=response.get("ResponseMetadata", {}).get("RequestId", "")
    )


def parse_aws_kms_decrypt_response(response: Dict[str, Any]) -> DecryptionResponse:
    """Parse AWS KMS decrypt API response into DecryptionResponse model."""
    plaintext = response.get("Plaintext", b"")
    if isinstance(plaintext, bytes):
        plaintext = plaintext.decode("utf-8", errors="replace")
    return DecryptionResponse(
        plaintext=plaintext,
        key_id=response.get("KeyId", ""),
        encryption_context=response.get("EncryptionContext", {}),
        request_id=response.get("ResponseMetadata", {}).get("RequestId", "")
    )


def parse_aws_kms_sign_response(response: Dict[str, Any]) -> SigningResponse:
    """Parse AWS KMS sign API response into SigningResponse model."""
    return SigningResponse(
        signature=encode_ciphertext(response.get("Signature", b"")),
        key_id=response.get("KeyId", ""),
        algorithm=response.get("SigningAlgorithm", ""),
        request_id=response.get("ResponseMetadata", {}).get("RequestId", "")
    )


def parse_aws_kms_verify_response(response: Dict[str, Any]) -> VerificationResponse:
    """Parse AWS KMS verify API response into VerificationResponse model."""
    return VerificationResponse(
        is_valid=response.get("SignatureValid", False),
        key_id=response.get("KeyId", ""),
        request_id=response.get("ResponseMetadata", {}).get("RequestId", "")
    )
