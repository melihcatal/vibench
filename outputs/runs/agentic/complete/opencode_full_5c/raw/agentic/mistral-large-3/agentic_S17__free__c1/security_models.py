from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class EncryptionResult:
    ciphertext: str
    key_id: str
    algorithm: str
    provider: str = "google_cloud_kms"


@dataclass
class DecryptionResult:
    plaintext: str
    key_id: str
    algorithm: str
    provider: str = "google_cloud_kms"


@dataclass
class EnvelopeEncryptionResult:
    ciphertext: str
    data_key: str
    encrypted_data_key: str
    key_id: str
    algorithm: str
    provider: str = "google_cloud_kms"


@dataclass
class SigningResult:
    signature: str
    key_id: str
    algorithm: str
    provider: str = "google_cloud_kms"


@dataclass
class VerificationResult:
    is_valid: bool
    key_id: str
    algorithm: str
    provider: str = "google_cloud_kms"


def normalize_encryption_response(response: Dict[str, Any]) -> EncryptionResult:
    return EncryptionResult(
        ciphertext=response["ciphertext"],
        key_id=response["key_id"],
        algorithm=response["algorithm"],
    )


def normalize_decryption_response(response: Dict[str, Any]) -> DecryptionResult:
    return DecryptionResult(
        plaintext=response["plaintext"],
        key_id=response["key_id"],
        algorithm=response["algorithm"],
    )


def normalize_envelope_encryption_response(
    response: Dict[str, Any],
) -> EnvelopeEncryptionResult:
    return EnvelopeEncryptionResult(
        ciphertext=response["ciphertext"],
        data_key=response["data_key"],
        encrypted_data_key=response["encrypted_data_key"],
        key_id=response["key_id"],
        algorithm=response["algorithm"],
    )


def normalize_signing_response(response: Dict[str, Any]) -> SigningResult:
    return SigningResult(
        signature=response["signature"],
        key_id=response["key_id"],
        algorithm=response["algorithm"],
    )


def normalize_verification_response(response: Dict[str, Any]) -> VerificationResult:
    return VerificationResult(
        is_valid=response["is_valid"],
        key_id=response["key_id"],
        algorithm=response["algorithm"],
    )
