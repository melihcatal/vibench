from typing import TypedDict


class EncryptRequest(TypedDict):
    """Payload for encrypt_payload function."""

    plaintext: str
    key_id: str


class EncryptResponse(TypedDict):
    """Payload returned by encrypt_payload function."""

    ciphertext: str
    key_id: str


class DecryptRequest(TypedDict):
    """Payload for decrypt_payload function."""

    ciphertext: str
    key_id: str


class DecryptResponse(TypedDict):
    """Payload returned by decrypt_payload function."""

    plaintext: str
    key_id: str


class EnvelopeEncryptRequest(TypedDict):
    """Payload for envelope_encrypt function."""

    plaintext: str
    key_id: str


class EnvelopeEncryptResponse(TypedDict):
    """Payload returned by envelope_encrypt function."""

    encrypted_data: bytes
    encrypted_data_key: bytes
    key_id: str
