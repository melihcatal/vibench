"""Encrypts a plaintext payload with a managed key using AWS KMS."""

import base64
from typing import Optional, Dict

from security_client import get_kms_client, ensure_binary, build_encryption_context
from security_models import EncryptRequest, EncryptResponse, normalize_encrypt_response


def encrypt_payload(
    plaintext: bytes,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
    region: str = "us-east-1",
) -> EncryptResponse:
    """Encrypt plaintext using AWS KMS managed key.

    Args:
        plaintext: The raw bytes to encrypt.
        key_id: AWS KMS key ID or alias.
        encryption_context: Optional KMS encryption context key-value pairs.
        region: AWS region for the KMS service.

    Returns:
        EncryptResponse containing the ciphertext blob and metadata.
    """
    kms = get_kms_client(region=region)
    plain = ensure_binary(plaintext)

    params = {
        "KeyId": key_id,
        "Plaintext": plain,
        "EncryptionAlgorithm": "SYMMETRIC_DEFAULT",
    }
    if encryption_context:
        params["EncryptionContext"] = encryption_context

    response = kms.encrypt(**params)

    raw = {
        "ciphertext_blob": response["CiphertextBlob"],
        "key_id": response["KeyId"],
        "encryption_algorithm": response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
        "encryption_context": response.get("EncryptionContext"),
    }
    return normalize_encrypt_response(raw)


if __name__ == "__main__":
    import os

    plaintext = b"Sensitive data to encrypt"
    key_id = os.environ.get("AWS_KMS_KEY_ID", "alias/default")
    result = encrypt_payload(plaintext, key_id)
    print(f"Key ID: {result.key_id}")
    print(f"Algorithm: {result.algorithm}")
    print(f"Ciphertext (base64): {base64.b64encode(result.ciphertext).decode('utf-8')}")
