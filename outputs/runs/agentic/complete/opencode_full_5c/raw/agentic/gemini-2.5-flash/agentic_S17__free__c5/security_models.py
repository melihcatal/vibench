from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class EncryptionRequest:
    """Defines a request structure for encryption operations."""

    plaintext: str
    key_name: str  # Full KMS key path or identifier


@dataclass
class EncryptionResponse:
    """Defines a response structure for encryption operations."""

    ciphertext: str
    key_version_used: Optional[str] = None


@dataclass
class DecryptionRequest:
    """Defines a request structure for decryption operations."""

    ciphertext: str
    key_name: str  # Full KMS key path or identifier


@dataclass
class DecryptionResponse:
    """Defines a response structure for decryption operations."""

    plaintext: str


@dataclass
class EnvelopeEncryptionRequest:
    """Defines a request structure for envelope encryption."""

    plaintext: str
    kek_name: str  # Key Encryption Key (KEK) name, typically a KMS key path


@dataclass
class EnvelopeEncryptionResponse:
    """Defines a response structure for envelope encryption."""

    encrypted_payload: str
    wrapped_dek: str  # Encrypted Data Encryption Key (DEK)


@dataclass
class SigningRequest:
    """Defines a request structure for signing operations."""

    message: str
    key_version_name: str  # Full KMS key version path for signing


@dataclass
class SigningResponse:
    """Defines a response structure for signing operations."""

    signature: str


@dataclass
class VerificationRequest:
    """Defines a request structure for signature verification."""

    message: str
    signature: str
    key_version_name: str  # Full KMS key version path to retrieve public key


@dataclass
class VerificationResponse:
    """Defines a response structure for signature verification."""

    is_valid: bool


@dataclass
class AuditLogEntry:
    """Normalized structure for a crypto-related audit log entry."""

    timestamp: str
    resource_name: str
    method_name: str
    principal_email: str
    severity: str
    json_payload: Dict[str, Any] = field(
        default_factory=dict
    )  # Original JSON payload for full context


@dataclass
class DlpScanRequest:
    """Request for DLP scanning."""

    text_content: str
    project_id: str
    min_likelihood: str = "POSSIBLE"  # e.g., POSSIBLE, LIKELY, VERY_LIKELY
    info_types: list[str] = field(
        default_factory=lambda: [
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "US_SOCIAL_SECURITY_NUMBER",
        ]
    )


@dataclass
class DlpScanResponse:
    """Response from DLP scanning."""

    findings: list[Dict[str, Any]] = field(default_factory=list)  # List of DLP findings


@dataclass
class EmbeddingRequest:
    """Request for text embedding."""

    text_content: str


@dataclass
class EmbeddingResponse:
    """Response from text embedding."""

    embedding: list[float]


@dataclass
class TranslationRequest:
    """Request for text translation."""

    text_content: str
    target_language_code: str
    project_id: str
    source_language_code: Optional[str] = None


@dataclass
class TranslationResponse:
    """Response from text translation."""

    translated_text: str


if __name__ == "__main__":
    print("This file defines data models for security-related operations.")
    # Example usage:
    # req = EncryptionRequest(plaintext="hello", key_name="projects/.../keys/...")
    # print(req)
