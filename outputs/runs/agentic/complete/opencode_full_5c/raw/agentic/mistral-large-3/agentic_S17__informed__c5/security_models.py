from typing import Dict, Any, Union, Optional
from dataclasses import dataclass


@dataclass
class EncryptRequest:
    key_id: str
    plaintext: bytes
    context: Optional[Dict[str, str]] = None


@dataclass
class EncryptResponse:
    ciphertext: bytes
    key_id: str
    algorithm: str
    context: Optional[Dict[str, str]] = None


@dataclass
class DecryptRequest:
    ciphertext: bytes
    context: Optional[Dict[str, str]] = None


@dataclass
class DecryptResponse:
    plaintext: bytes
    key_id: str
    algorithm: str
    context: Optional[Dict[str, str]] = None


@dataclass
class DataKeyRequest:
    key_id: str
    key_spec: str = "AES_256"


@dataclass
class DataKeyResponse:
    plaintext_key: bytes
    ciphertext_key: bytes
    key_id: str


@dataclass
class SignRequest:
    key_id: str
    message: bytes
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256"


@dataclass
class SignResponse:
    signature: bytes
    key_id: str
    signing_algorithm: str


@dataclass
class VerifyRequest:
    key_id: str
    message: bytes
    signature: bytes
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256"


@dataclass
class VerifyResponse:
    signature_valid: bool
    key_id: str


def normalize_encrypt_response(response: Dict[str, Any]) -> EncryptResponse:
    return EncryptResponse(
        ciphertext=response["ciphertext"],
        key_id=response["key_id"],
        algorithm=response.get("algorithm", "Unknown"),
    )


def normalize_decrypt_response(response: Dict[str, Any]) -> DecryptResponse:
    return DecryptResponse(
        plaintext=response["plaintext"],
        key_id=response["key_id"],
        algorithm=response.get("algorithm", "Unknown"),
    )


def normalize_data_key_response(response: Dict[str, Any]) -> DataKeyResponse:
    return DataKeyResponse(
        plaintext_key=response["plaintext_key"],
        ciphertext_key=response["ciphertext_key"],
        key_id=response["key_id"],
    )


def normalize_sign_response(response: Dict[str, Any]) -> SignResponse:
    return SignResponse(
        signature=response["signature"],
        key_id=response["key_id"],
        signing_algorithm=response.get("signing_algorithm", "Unknown"),
    )


def normalize_verify_response(response: Dict[str, Any]) -> VerifyResponse:
    return VerifyResponse(
        signature_valid=response["signature_valid"], key_id=response["key_id"]
    )
