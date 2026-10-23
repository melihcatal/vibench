"""
envelope_encrypt.py - Implements envelope encryption using AWS KMS and local AES-GCM.

Uses AWS KMS GenerateDataKey API to obtain a plaintext data key and its encrypted form.
The plaintext data key is used locally with the cryptography library (AES-256-GCM)
to encrypt the actual payload. The encrypted data key and ciphertext are returned
together, implementing the envelope encryption pattern.

Provider: AWS KMS (boto3 client for kms.us-east-1.amazonaws.com)
Key Type: AES_256 data key via KMS GenerateDataKey
"""

import base64
import json
import logging
import os
import sys
from typing import Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import get_kms_client, load_encryption_context, validate_key_id
from security_models import (
    EnvelopeEncryptionRequest,
    EnvelopeEncryptionResponse,
    encode_ciphertext,
    normalize_envelope_response,
)

logger = logging.getLogger(__name__)

KMS_KEY_SPEC = os.environ.get("ENVELOPE_KEY_SPEC", "AES_256")


def generate_data_key(kms_client, key_id: str, key_spec: str = "AES_256") -> dict:
    """
    Call AWS KMS GenerateDataKey API to get a plaintext and encrypted data key pair.

    Returns dict with Plaintext (bytes), CiphertextBlob (bytes), and KeyId.
    """
    try:
        response = kms_client.generate_data_key(
            KeyId=key_id,
            KeySpec=key_spec,
        )
        return response
    except Exception as e:
        raise RuntimeError(f"AWS KMS GenerateDataKey failed: {e}") from e


def encrypt_with_data_key(plaintext: str, data_key_bytes: bytes) -> dict:
    """
    Encrypt plaintext locally using AES-256-GCM with the provided data key.

    Returns dict with nonce and ciphertext (both base64-encoded).
    """
    aesgcm = AESGCM(data_key_bytes)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    return {
        "nonce": base64.b64encode(nonce).decode("utf-8"),
        "ciphertext": base64.b64encode(ct).decode("utf-8"),
    }


def envelope_encrypt(
    plaintext: str,
    key_id: str,
    encryption_context: Optional[str] = None,
    region: Optional[str] = None,
    key_spec: str = "AES_256",
) -> EnvelopeEncryptionResponse:
    """
    Perform envelope encryption using AWS KMS and local AES-GCM.

    Steps:
        1. Call KMS GenerateDataKey to get a plaintext + encrypted data key pair.
        2. Use the plaintext data key to AES-256-GCM encrypt the payload locally.
        3. Combine the encrypted data key, nonce, and ciphertext into the response.

    Args:
        plaintext: The plaintext string to encrypt.
        key_id: The KMS CMK ID, ARN, or alias for wrapping the data key.
        encryption_context: Optional JSON string for KMS encryption context.
        region: AWS region override.
        key_spec: KMS data key spec, e.g., AES_256.

    Returns:
        EnvelopeEncryptionResponse with encrypted data key, combined ciphertext blob, and metadata.

    Raises:
        RuntimeError: If KMS or local encryption fails.
    """
    validate_key_id(key_id)
    kms_client = get_kms_client(region_name=region)
    encryption_ctx = load_encryption_context(encryption_context)

    generate_kwargs: dict = {"KeyId": key_id, "KeySpec": key_spec}
    if encryption_ctx:
        generate_kwargs["EncryptionContext"] = encryption_ctx

    data_key_response = generate_data_key(kms_client, key_id, key_spec)

    plaintext_data_key = data_key_response["Plaintext"]
    encrypted_data_key_bytes = data_key_response["CiphertextBlob"]
    encrypted_data_key = encode_ciphertext(encrypted_data_key_bytes)

    local_result = encrypt_with_data_key(plaintext, plaintext_data_key)

    combined_payload = json.dumps({
        "nonce": local_result["nonce"],
        "ciphertext": local_result["ciphertext"],
        "encrypted_data_key": encrypted_data_key,
        "key_id": data_key_response.get("KeyId", key_id),
        "encryption_context": encryption_ctx,
    })

    response = normalize_envelope_response(
        data_key_response=data_key_response,
        encrypted_data_key=encrypted_data_key,
        ciphertext=base64.b64encode(combined_payload.encode("utf-8")).decode("utf-8"),
        key_id=key_id,
    )

    logger.info(
        "Envelope encryption complete with KMS key %s, key_spec %s",
        response.key_id,
        key_spec,
    )
    return response


def main():
    """CLI entry point for envelope_encrypt."""
    if len(sys.argv) < 3:
        print("Usage: python envelope_encrypt.py <key_id> <plaintext> [encryption_context_json]")
        sys.exit(1)

    key_id = sys.argv[1]
    plaintext = sys.argv[2]
    context = sys.argv[3] if len(sys.argv) > 3 else None

    logging.basicConfig(level=logging.INFO)
    result = envelope_encrypt(plaintext, key_id, encryption_context=context)

    output = {
        "encrypted_data_key": result.encrypted_data_key,
        "ciphertext_blob": result.ciphertext_blob,
        "key_id": result.key_id,
        "algorithm": result.algorithm,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
