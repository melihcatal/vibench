# [HELPER] security_models.py
from __future__ import annotations
from typing import TypedDict, Optional

# Request/response normalization helpers


class KmsEncryptRequest(TypedDict):
    plaintext: str
    key_name: str


class KmsEncryptResponse(TypedDict):
    ciphertext: bytes
    algorithm: str
    key_id: str
    provider: str


class KmsDecryptRequest(TypedDict):
    ciphertext: bytes
    algorithm: Optional[str]
    key_id: Optional[str]


class KmsDecryptResponse(TypedDict):
    plaintext: str


class EnvelopeEncryptionRequest(TypedDict):
    plaintext: str
    data_key_id: str


class EnvelopeEncryptionResponse(TypedDict):
    encrypted_data: bytes
    encrypted_data_key: bytes
    data_key_id: str
    provider: str


# Normalization utilities


def normalize_kms_request(payload: dict) -> KmsEncryptRequest:
    """Converts a generic dict into a typed KmsEncryptRequest."""
    return KmsEncryptRequest(**payload)


def normalize_kms_response(response: Any) -> KmsEncryptResponse:
    """Converts an arbitrary response object into our normalized response."""
    return KmsEncryptResponse(
        ciphertext=response.ciphertext,
        algorithm=response.algorithm,
        key_id=response.key_id,
        provider="azure-key-vault",
    )
