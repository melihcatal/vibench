from typing import Dict, Any, Union, Optional
from dataclasses import dataclass


@dataclass
class EncryptionResult:
    ciphertext: bytes
    key_id: str
    encryption_algorithm: Optional[str] = None
    iv: Optional[bytes] = None
    tag: Optional[bytes] = None


@dataclass
class DecryptionResult:
    plaintext: bytes
    key_id: str
    encryption_algorithm: Optional[str] = None


@dataclass
class DataKeyResult:
    ciphertext_key: bytes
    plaintext_key: bytes
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
    model_id: str
    dimensions: int


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str


def normalize_encryption_response(response: Dict[str, Any]) -> EncryptionResult:
    return EncryptionResult(
        ciphertext=response["ciphertext"],
        key_id=response["key_id"],
        encryption_algorithm=response.get("encryption_algorithm"),
    )


def normalize_decryption_response(response: Dict[str, Any]) -> DecryptionResult:
    return DecryptionResult(
        plaintext=response["plaintext"],
        key_id=response["key_id"],
        encryption_algorithm=response.get("encryption_algorithm"),
    )


def normalize_data_key_response(response: Dict[str, Any]) -> DataKeyResult:
    return DataKeyResult(
        ciphertext_key=response["ciphertext_key"],
        plaintext_key=response["plaintext_key"],
        key_id=response["key_id"],
    )


def normalize_signing_response(response: Dict[str, Any]) -> SigningResult:
    return SigningResult(
        signature=response["signature"],
        key_id=response["key_id"],
        signing_algorithm=response["signing_algorithm"],
    )


def normalize_verification_response(response: Dict[str, Any]) -> VerificationResult:
    return VerificationResult(
        signature_valid=response["signature_valid"], key_id=response["key_id"]
    )
