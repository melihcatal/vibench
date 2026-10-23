"""Decrypts a ciphertext payload with a managed key using AWS KMS."""

import base64
from typing import Optional, Dict

from security_client import get_kms_client, ensure_binary, build_encryption_context
from security_models import DecryptRequest, DecryptResponse, normalize_decrypt_response


def decrypt_payload(
    ciphertext: bytes,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    region: str = "us-east-1",
) -> DecryptResponse:
    """Decrypt ciphertext using AWS KMS managed key.

    The key ID is embedded in the KMS ciphertext blob, so it can be
    optionally provided. If supplied, KMS verifies the key matches.

    Args:
        ciphertext: The raw ciphertext bytes from KMS encrypt.
        key_id: Optional KMS key ID for verification.
        encryption_context: Optional KMS encryption context (must match encryption).
        region: AWS region for the KMS service.

    Returns:
        DecryptResponse containing the plaintext bytes and metadata.
    """
    kms = get_kms_client(region=region)

    params = {
        "CiphertextBlob": ciphertext,
    }
    if key_id:
        params["KeyId"] = key_id
    if encryption_context:
        params["EncryptionContext"] = encryption_context

    response = kms.decrypt(**params)

    raw = {
        "plaintext": response["Plaintext"],
        "key_id": response.get("KeyId", ""),
        "encryption_algorithm": response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
    }
    return normalize_decrypt_response(raw)


if __name__ == "__main__":
    import os

    # Example: decrypt a base64-encoded ciphertext blob
    ciphertext_b64 = os.environ.get("ENCRYPTED_PAYLOAD", "")
    if ciphertext_b64:
        ciphertext = base64.b64decode(ciphertext_b64)
        result = decrypt_payload(ciphertext)
        print(f"Decrypted plaintext: {result.plaintext.decode('utf-8')}")
        print(f"Key ID used: {result.key_id}")
