# security_models.py
from typing import TypedDict, Optional

class EncryptionRequest(TypedDict):
    """Request model for encrypting data."""
    plaintext: str
    key_name: str  # Full resource name, e.g. projects/*/locations/*/keyRings/*/cryptoKeys/*

class EncryptionResponse(TypedDict):
    """Response model for encrypting data."""
    ciphertext: bytes
    name: str

class DecryptionRequest(TypedDict):
    """Request model for decrypting data."""
    ciphertext: str  # Base64 encoded ciphertext
    name: str

class DecryptionResponse(TypedDict):
    """Response model for decrypting data."""
    plaintext: str

class EnvelopeEncryptionRequest(TypedDict):
    """Request model for envelope encryption (data key + ciphertext)."""
    plaintext: str
    key_name: str

class EnvelopeEncryptionResponse(TypedDict):
    """Response model for envelope encryption."""
    ciphertext: bytes
    iv: bytes
    wrapped_key: bytes
    key_name: str

class SignRequest(TypedDict):
    """Request model for signing data with an asymmetric key."""
    plaintext: str
    key_name: str

class SignResponse(TypedDict):
    """Response model for signing data."""
    signature: bytes

class VerifyRequest(TypedDict):
    """Request model for verifying a signature."""
    signature_b64: str  # Base64 encoded signature expected for demo
    plaintext: str
    key_name: str

class VerifyResponse(TypedDict):
    """Response model for signature verification."""
    success: bool

# Normalizer helpers (simple)\n\ndef normalize_key_name(name: str) -> str:
    """Ensure the key name follows Google Cloud KMS format. Placeholder for other providers."""
    return name.strip()

# Utils for payload normalization\n\ndef to_bytes(data: str) -> bytes:
    return data.encode('utf-8')\n\ndef from_bytes(data: bytes) -> str:
    return data.decode('utf-8')\n