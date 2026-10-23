from dataclasses import dataclass
from typing import Optional, Any, Dict, List
from datetime import datetime


@dataclass
class EncryptionRequest:
    plaintext: str
    key_id: str


@dataclass
class EncryptionResponse:
    success: bool
    ciphertext: Optional[bytes] = None
    key_id: Optional[str] = None
    algorithm: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None


@dataclass
class DecryptionRequest:
    ciphertext: bytes
    key_id: str


@dataclass
class DecryptionResponse:
    success: bool
    plaintext: Optional[str] = None
    key_id: Optional[str] = None
    algorithm: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None


@dataclass
class EnvelopeEncryptionRequest:
    plaintext: str
    key_id: str


@dataclass
class EnvelopeEncryptionResponse:
    success: bool
    encrypted_data_key: Optional[bytes] = None
    ciphertext: Optional[bytes] = None
    iv: Optional[bytes] = None
    key_id: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None


@dataclass
class SignRequest:
    message: str
    key_id: str


@dataclass
class SignResponse:
    success: bool
    signature: Optional[bytes] = None
    key_id: Optional[str] = None
    algorithm: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None


@dataclass
class VerifyRequest:
    message: str
    signature: bytes
    key_id: str


@dataclass
class VerifyResponse:
    success: bool
    is_valid: Optional[bool] = None
    key_id: Optional[str] = None
    algorithm: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None


@dataclass
class KeyUsageSummary:
    key_id: str
    operation_count: int
    last_used: Optional[datetime] = None
    provider: Optional[str] = None


@dataclass
class SafetyCheckRequest:
    text: str


@dataclass
class SafetyCheckResponse:
    is_safe: bool
    scores: Optional[Dict[str, float]] = None
    categories: Optional[List[str]] = None
    provider: Optional[str] = None
    error: Optional[str] = None


@dataclass
class EmbeddingRequest:
    text: str


@dataclass
class EmbeddingResponse:
    success: bool
    embedding: Optional[List[float]] = None
    model: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class TranslationResponse:
    success: bool
    translated_text: Optional[str] = None
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None
