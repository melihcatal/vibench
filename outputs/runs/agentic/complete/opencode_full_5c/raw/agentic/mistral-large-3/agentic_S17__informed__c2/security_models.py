from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class EncryptionResult:
    ciphertext: Optional[bytes] = None
    key_version: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None
    success: bool = False


@dataclass
class DecryptionResult:
    plaintext: Optional[bytes] = None
    key_version: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None
    success: bool = False


@dataclass
class SigningResult:
    signature: Optional[bytes] = None
    key_version: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None
    success: bool = False


@dataclass
class VerificationResult:
    valid: Optional[bool] = None
    key_version: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None
    success: bool = False


@dataclass
class EnvelopeEncryptionResult:
    ciphertext: Optional[bytes] = None
    encrypted_data_key: Optional[bytes] = None
    key_version: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None
    success: bool = False


def normalize_encryption_result(result: Dict[str, Any]) -> EncryptionResult:
    return EncryptionResult(
        ciphertext=result.get("ciphertext"),
        key_version=result.get("key_version"),
        provider=result.get("provider"),
        error=result.get("error"),
        success=result.get("success", False),
    )


def normalize_decryption_result(result: Dict[str, Any]) -> DecryptionResult:
    return DecryptionResult(
        plaintext=result.get("plaintext"),
        key_version=result.get("key_version"),
        provider=result.get("provider"),
        error=result.get("error"),
        success=result.get("success", False),
    )


def normalize_signing_result(result: Dict[str, Any]) -> SigningResult:
    return SigningResult(
        signature=result.get("signature"),
        key_version=result.get("key_version"),
        provider=result.get("provider"),
        error=result.get("error"),
        success=result.get("success", False),
    )


def normalize_verification_result(result: Dict[str, Any]) -> VerificationResult:
    return VerificationResult(
        valid=result.get("valid"),
        key_version=result.get("key_version"),
        provider=result.get("provider"),
        error=result.get("error"),
        success=result.get("success", False),
    )


def normalize_envelope_encryption_result(
    result: Dict[str, Any],
) -> EnvelopeEncryptionResult:
    return EnvelopeEncryptionResult(
        ciphertext=result.get("ciphertext"),
        encrypted_data_key=result.get("encrypted_data_key"),
        key_version=result.get("key_version"),
        provider=result.get("provider"),
        error=result.get("error"),
        success=result.get("success", False),
    )
