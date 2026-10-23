from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class EncryptionResult:
    ciphertext: bytes
    key_id: str
    algorithm: str
    iv: Optional[bytes] = None
    tag: Optional[bytes] = None


@dataclass
class DecryptionResult:
    plaintext: bytes
    key_id: str
    algorithm: str


@dataclass
class DataKeyResult:
    plaintext_key: bytes
    ciphertext_key: bytes
    key_id: str


@dataclass
class SigningResult:
    signature: bytes
    key_id: str
    signing_algorithm: str


@dataclass
class VerificationResult:
    signature_valid: bool
    key_id: str


@dataclass
class EnvelopeEncryptionResult:
    ciphertext: bytes
    encrypted_data_key: bytes
    iv: bytes
    tag: Optional[bytes] = None
    key_id: Optional[str] = None


@dataclass
class KeyUsageEvent:
    key_id: str
    operation: str
    status: str
    timestamp: str
    metadata: Dict[str, Any]


@dataclass
class SafetyCheckResult:
    is_safe: bool
    violations: Dict[str, Any]
    confidence: float


@dataclass
class EmbeddingResult:
    embedding: list
    model: str
    dimensions: int


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str
