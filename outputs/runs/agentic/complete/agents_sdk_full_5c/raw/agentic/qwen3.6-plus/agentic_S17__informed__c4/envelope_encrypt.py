"""Implements envelope encryption using AWS KMS managed key service."""

import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from typing import Optional, Dict

from security_client import get_kms_client, ensure_binary, build_encryption_context
from security_models import (
    EnvelopeEncryptRequest,
    EnvelopeEncryptResponse,
    normalize_envelope_response,
)


def envelope_encrypt(
    plaintext: bytes,
    key_id: str,
    key_spec: str = "AES_256",
    encryption_context: Optional[Dict[str, str]] = None,
    region: str = "us-east-1",
) -> EnvelopeEncryptResponse:
    """Perform envelope encryption using AWS KMS.

    Envelope encryption flow:
    1. KMS generates a plaintext data key, returning both plaintext and
       encrypted copies.
    2. Locally encrypt the payload with the plaintext data key using AES-256-GCM.
    3. Return the encrypted data key + encrypted payload.

    The encrypted data key can be safely stored alongside the ciphertext.
    Decryption requires calling KMS Decrypt on the encrypted data key first.

    Args:
        plaintext: Raw bytes to encrypt.
        key_id: AWS KMS customer master key ID or alias.
        key_spec: KMS key spec (e.g., AES_256, AES_128).
        encryption_context: Optional KMS encryption context.
        region: AWS region.

    Returns:
        EnvelopeEncryptResponse with encrypted_data_key and ciphertext.
    """
    kms = get_kms_client(region=region)
    plain = ensure_binary(plaintext)

    generate_params = {
        "KeyId": key_id,
        "KeySpec": key_spec if key_spec.startswith("AES") else "AES_256",
    }
    if encryption_context:
        generate_params["EncryptionContext"] = encryption_context

    data_key_resp = kms.generate_data_key(**generate_params)
    plaintext_data_key = data_key_resp["Plaintext"]
    encrypted_data_key = data_key_resp["CiphertextBlob"]

    # Use AES-256-GCM with a random nonce for local encryption
    nonce = os.urandom(12)
    aesgcm = AESGCM(plaintext_data_key)
    ciphertext = nonce + aesgcm.encrypt(nonce, plain, None)

    algorithm = "AES_256_GCM"
    if "128" in key_spec:
        algorithm = "AES_128_GCM"

    raw = {
        "encrypted_data_key": encrypted_data_key,
        "ciphertext": ciphertext,
        "key_id": data_key_resp["KeyId"],
        "algorithm": algorithm,
        "encryption_context": encryption_context,
    }
    return normalize_envelope_response(raw)


if __name__ == "__main__":
    import os

    plaintext = b"Highly sensitive data for envelope encryption"
    key_id = os.environ.get("AWS_KMS_KEY_ID", "alias/default")
    result = envelope_encrypt(plaintext, key_id)
    print(f"Key ID: {result.key_id}")
    print(f"Algorithm: {result.algorithm}")
    print(f"Encrypted Data Key (base64): {base64.b64encode(result.encrypted_data_key).decode('utf-8')}")
    print(f"Ciphertext (base64): {base64.b64encode(result.ciphertext).decode('utf-8')}")
