from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class ProviderType(Enum):
    AWS_KMS = "aws_kms"
    AZURE_KEY_VAULT = "azure_key_vault"
    GOOGLE_KMS = "google_kms"
    HASHICORP_VAULT = "hashicorp_vault"


@dataclass
class EncryptionRequest:
    plaintext: str
    key_id: str
    algorithm: Optional[str] = None


@dataclass
class EncryptionResponse:
    success: bool
    ciphertext: Optional[str] = None
    key_id: Optional[str] = None
    algorithm: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None


@dataclass
class DecryptionRequest:
    ciphertext: str
    key_id: str
    algorithm: Optional[str] = None


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
    algorithm: Optional[str] = None


@dataclass
class EnvelopeEncryptionResponse:
    success: bool
    encrypted_data_key: Optional[str] = None
    iv: Optional[str] = None
    ciphertext: Optional[str] = None
    key_id: Optional[str] = None
    algorithm: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None


@dataclass
class SignRequest:
    data: str
    key_id: str
    algorithm: Optional[str] = None


@dataclass
class SignResponse:
    success: bool
    signature: Optional[str] = None
    key_id: Optional[str] = None
    algorithm: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None


@dataclass
class VerifyRequest:
    data: str
    signature: str
    key_id: str
    algorithm: Optional[str] = None


@dataclass
class VerifyResponse:
    success: bool
    valid: Optional[bool] = None
    key_id: Optional[str] = None
    algorithm: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None


@dataclass
class KeyUsageSummary:
    key_id: str
    provider: str
    encryption_count: int = 0
    decryption_count: int = 0
    signing_count: int = 0
    verification_count: int = 0
    last_used: Optional[str] = None


@dataclass
class SafetyCheckResult:
    is_safe: bool
    categories: Dict[str, float]
    provider: str
    error: Optional[str] = None


@dataclass
class EmbeddingResult:
    success: bool
    embedding: Optional[list] = None
    provider: str = None
    error: Optional[str] = None


@dataclass
class TranslationResult:
    success: bool
    translated_text: Optional[str] = None
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None
    provider: str = None
    error: Optional[str] = None
