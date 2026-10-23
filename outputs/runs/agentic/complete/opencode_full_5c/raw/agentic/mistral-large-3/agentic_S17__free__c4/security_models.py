from typing import Dict, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class EncryptionResult:
    ciphertext: bytes
    key_version: str
    algorithm: str
    additional_authenticated_data: Optional[bytes] = None


@dataclass
class DecryptionResult:
    plaintext: bytes
    key_version: str
    algorithm: str


@dataclass
class SigningResult:
    signature: bytes
    key_version: str
    algorithm: str


@dataclass
class VerificationResult:
    is_valid: bool
    key_version: str
    algorithm: str


def normalize_encryption_response(response: Dict[str, Any]) -> EncryptionResult:
    return EncryptionResult(
        ciphertext=response["ciphertext"],
        key_version=response["name"].split("/")[-1],
        algorithm=response.get("algorithm", "AES_256_GCM"),
    )


def normalize_decryption_response(response: Dict[str, Any]) -> DecryptionResult:
    return DecryptionResult(
        plaintext=response["plaintext"],
        key_version=response["name"].split("/")[-1],
        algorithm=response.get("algorithm", "AES_256_GCM"),
    )


def normalize_signing_response(response: Dict[str, Any]) -> SigningResult:
    return SigningResult(
        signature=response["signature"],
        key_version=response["name"].split("/")[-1],
        algorithm=response.get("algorithm", "RSA_SIGN_PSS_2048_SHA256"),
    )


def normalize_verification_response(response: Dict[str, Any]) -> VerificationResult:
    return VerificationResult(
        is_valid=response["verified"],
        key_version=response["name"].split("/")[-1],
        algorithm=response.get("algorithm", "RSA_SIGN_PSS_2048_SHA256"),
    )


def serialize_payload(payload: Any) -> bytes:
    if isinstance(payload, bytes):
        return payload
    elif isinstance(payload, str):
        return payload.encode("utf-8")
    else:
        return json.dumps(payload).encode("utf-8")


def deserialize_payload(payload: bytes) -> Any:
    try:
        return json.loads(payload.decode("utf-8"))
    except json.JSONDecodeError:
        return payload.decode("utf-8")
