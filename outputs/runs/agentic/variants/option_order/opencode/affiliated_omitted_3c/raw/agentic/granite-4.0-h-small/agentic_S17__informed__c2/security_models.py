# [HELPER] security_models.py - Define local request, response, and normalization helpers for Key Management and Encryption

from typing import Any, Dict, List, Optional

# Base request model for encrypt/decrypt operations
EncryptRequest = Dict[str, Any]
DecryptRequest = Dict[str, Any]


def normalize_encrypt_input(data: str) -> EncryptRequest:
    """Converts raw plaintext into a structured request ready for any provider.

    Args:
        data: Plaintext string to encrypt.

    Returns:
        Dict containing normalized fields (e.g., payload, optional metadata).
    """
    return {
        "service": "generic",
        "payload": data,
        "metadata": {
            "format": "utf-8",
            "type": "plaintext",
        },
    }


def normalize_decrypt_input(ciphertext: str) -> DecryptRequest:
    """Converts raw ciphertext into a structured request ready for any provider.

    Args:
        ciphertext: Ciphertext string returned by an encrypt operation.

    Returns:
        Dict containing normalized fields for decryption.
    """
    return {
        "service": "generic",
        "ciphertext": ciphertext,
        "metadata": {
            "format": "utf-8",
            "type": "ciphertext",
        },
    }


def denormalize_response(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Flattens a provider-specific response into a common shape.

    Expected common fields:
        - service: string name of the provider
        - payload: the decrypted plaintext (or ciphertext for wrap/unwrap)
        - metadata: dict of auxiliary info
    """
    # Most SDKs already return a flat dict; ensure keys are present with defaults
    return {
        "service": raw.get("service", "unknown"),
        "payload": raw.get("payload", raw.get("plaintext", raw.get("ciphertext", ""))),
        "metadata": raw.get("metadata", {}),
    }


# Example helper for envelope encryption – generate a random data key
import os


def generate_data_key(length: int = 32) -> bytes:
    """Generates a cryptographically secure random data encryption key (DEK)."""
    return os.urandom(length)


# Simple envelope encryption utility (independent of provider)
def local_envelope_encrypt(plaintext: str, dek: bytes) -> Dict[str, Any]:
    """Local AES-GCM envelope encryption using cryptography library.
    Does NOT use any managed key service.
    """
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.backends import default_backend
    import json

    iv = os.urandom(12)
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(dek), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded) + encryptor.finalize()
    tag = encryptor.tag
    return {
        "encrypted_data": {
            "ciphertext": ct.hex(),
            "iv": iv.hex(),
            "tag": tag.hex(),
        },
        "metadata": {
            "algorithm": "AES-256-GCM",
        },
    }


if __name__ == "__main__":
    # Quick demo of normalization utilities
    print(
        "Normalized encrypt request:",
        json.dumps(normalize_encrypt_input("Hello"), indent=2),
    )
    print(
        "Normalized decrypt request:",
        json.dumps(normalize_decrypt_input("<<CIPHERTEXT>>"), indent=2),
    )
