from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class EncryptionRequest:
    plaintext: bytes
    key_id: str
    key_ring_id: Optional[str] = None
    location_id: Optional[str] = None
    project_id: Optional[str] = None


@dataclass
class EncryptionResponse:
    ciphertext: bytes
    encrypted_dek: Optional[bytes] = None  # For envelope encryption


@dataclass
class DecryptionRequest:
    ciphertext: bytes
    key_id: str
    key_ring_id: Optional[str] = None
    location_id: Optional[str] = None
    project_id: Optional[str] = None
    encrypted_dek: Optional[bytes] = None  # For envelope encryption


@dataclass
class DecryptionResponse:
    plaintext: bytes


@dataclass
class SigningRequest:
    payload: bytes
    key_id: str
    key_ring_id: Optional[str] = None
    location_id: Optional[str] = None
    project_id: Optional[str] = None
    key_version_id: Optional[str] = None


@dataclass
class SigningResponse:
    signature: bytes


@dataclass
class VerificationRequest:
    payload: bytes
    signature: bytes
    key_id: str
    key_ring_id: Optional[str] = None
    location_id: Optional[str] = None
    project_id: Optional[str] = None
    key_version_id: Optional[str] = None


@dataclass
class VerificationResponse:
    is_valid: bool


@dataclass
class ContentSafetyRequest:
    text: str
    categories: Optional[list[str]] = field(
        default_factory=lambda: ["Hate", "Sexual", "SelfHarm", "Violence"]
    )


@dataclass
class ContentSafetyResponse:
    is_safe: bool
    detection_results: Optional[Dict[str, Any]] = None


@dataclass
class EmbeddingRequest:
    text: str
    model: str = "models/embedding-001"


@dataclass
class EmbeddingResponse:
    embedding: list[float]


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None
    project_id: Optional[str] = None


@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language: Optional[str] = None
