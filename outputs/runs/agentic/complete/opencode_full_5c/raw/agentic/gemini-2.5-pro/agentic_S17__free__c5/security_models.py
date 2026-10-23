from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class EncryptionRequest:
    key_name: str
    plaintext: bytes


@dataclass
class EncryptionResponse:
    key_name: str
    ciphertext: bytes


@dataclass
class DecryptionRequest:
    key_name: str
    ciphertext: bytes


@dataclass
class DecryptionResponse:
    key_name: str
    plaintext: bytes


@dataclass
class EnvelopeEncryptionRequest:
    key_name: str
    plaintext: bytes


@dataclass
class EnvelopeEncryptionResponse:
    wrapped_dek: bytes
    ciphertext: bytes


@dataclass
class SigningRequest:
    key_name: str
    data_to_sign: bytes


@dataclass
class SigningResponse:
    signature: bytes


@dataclass
class VerificationRequest:
    key_name: str
    data: bytes
    signature: bytes


@dataclass
class VerificationResponse:
    is_valid: bool


@dataclass
class KeyUsageEntry:
    timestamp: str
    principal_email: str
    method_name: str
    resource_name: str


@dataclass
class ContentSafetyRequest:
    text: str


@dataclass
class ContentSafetyResponse:
    scores: Dict[str, float]


@dataclass
class EmbeddingRequest:
    content: str


@dataclass
class EmbeddingResponse:
    embedding: List[float]


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None
