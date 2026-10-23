from typing import TypedDict, Any


class EncryptRequest(TypedDict):
    plaintext: str
    key_id: str


class EncryptResponse(TypedDict):
    CiphertextBlob: bytes
    KeyId: str
    EncryptionAlgorithm: str


class DecryptRequest(TypedDict):
    ciphertext_blob: bytes
    key_id: str


class DecryptResponse(TypedDict):
    Plaintext: bytes


class EnvelopeEncryptRequest(TypedDict):
    plaintext: str
    data_key: str  # Identifier of the Vault data key


class EnvelopeEncryptResponse(TypedDict):
    EncryptedDataKey: bytes
    EncryptedPlaintext: bytes


class SignRequest(TypedDict):
    key_id: str
    data: bytes


class SignResponse(TypedDict):
    Signature: bytes


class VerifyRequest(TypedDict):
    key_id: str
    signature: bytes
    data: bytes


class VerifyResponse(TypedDict):
    Valid: bool


# Normalization helpers\n
def normalize_encrypt_input(req: dict) -> EncryptRequest:
    """Ensure keys exist and types are correct."""
    return EncryptRequest(**req)


def normalize_decrypt_input(req: dict) -> DecryptRequest:
    return DecryptRequest(**req)


# ... additional helpers for envelope, sign/verify can be added as needed
