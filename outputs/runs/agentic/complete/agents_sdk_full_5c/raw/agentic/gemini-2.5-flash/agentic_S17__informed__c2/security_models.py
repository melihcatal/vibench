from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class EncryptionRequest:
    plaintext_data: bytes

@dataclass
class EncryptionResult:
    ciphertext_data: bytes

@dataclass
class DecryptionRequest:
    ciphertext_data: bytes

@dataclass
class DecryptionResult:
    plaintext_data: bytes

@dataclass
class EnvelopeEncryptionRequest:
    plaintext_data: bytes

@dataclass
class EnvelopeEncryptionResult:
    encrypted_data_encryption_key: bytes
    locally_encrypted_payload: bytes # The payload encrypted with the DEK locally

@dataclass
class SigningRequest:
    data_to_sign: bytes

@dataclass
class SigningResult:
    signature: bytes

@dataclass
class VerificationRequest:
    original_data: bytes
    signature: bytes

@dataclass
class VerificationResult:
    is_valid: bool

@dataclass
class KeyUsageEvent:
    key_id: str
    operation: str  # e.g., "ENCRYPT", "DECRYPT", "SIGN"
    timestamp: str  # ISO format string
    user_id: Optional[str] = None
    success: bool = True

@dataclass
class KeyUsageSummary:
    total_operations: int
    successful_operations: int
    failed_operations: int
    most_used_key: Optional[str] = None
    least_used_key: Optional[str] = None
    operations_by_key: dict = field(default_factory=dict)
    operations_by_user: dict = field(default_factory=dict)

@dataclass
class ContentSafetyRequest:
    text_content: str

@dataclass
class ContentSafetyResult:
    is_safe: bool
    scores: dict = field(default_factory=dict)
    unsafe_categories: List[str] = field(default_factory=list)

@dataclass
class EmbeddingRequest:
    text: str

@dataclass
class EmbeddingResult:
    embedding: List[float]

@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None

@dataclass
class TranslationResult:
    translated_text: str
    detected_source_language: Optional[str] = None
