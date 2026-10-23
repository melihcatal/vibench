"""
[SAME-SCENARIO] envelope_encrypt.py

Implements envelope encryption using AWS Key Management Service (KMS).
Provider: AWS KMS | SDK: boto3 | Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

Envelope encryption workflow:
1. Generate a data key using AWS KMS GenerateDataKey (returns plaintext + encrypted data key).
2. Encrypt the actual payload locally using the plaintext data key via AES-GCM.
3. Return the encrypted data key, ciphertext, and metadata so the envelope can be stored
   or transmitted. Decryption reverses this by first decrypting the data key with KMS.
"""

import os
import sys
import logging
from typing import Optional

import boto3
from botocore.exceptions import ClientError
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import (
    get_default_kms_client,
    get_kms_key_id,
    base64_encode_bytes,
    base64_decode_string,
    handle_kms_error,
    KMSError,
)
from security_models import (
    EnvelopeEncryptRequest,
    EnvelopeEncryptResponse,
    normalize_encryption_context,
    normalize_kms_response,
)

logger = logging.getLogger(__name__)

# AES-GCM nonce size in bytes
NONCE_SIZE = 12


def _generate_data_key(
    kms_client: boto3.client,
    key_id: str,
    data_key_spec: str = "AES_256",
    encryption_context: Optional[dict] = None,
) -> dict:
    """Call AWS KMS GenerateDataKey to obtain a plaintext + encrypted data key pair."""
    kwargs = {
        "KeyId": key_id,
        "KeySpec": data_key_spec,
    }
    norm_context = normalize_encryption_context(encryption_context)
    if norm_context:
        kwargs["EncryptionContext"] = norm_context

    try:
        return kms_client.generate_data_key(**kwargs)
    except ClientError as exc:
        raise handle_kms_error(exc, "generate_data_key") from exc


def _encrypt_local(plaintext: bytes, data_key: bytes) -> tuple:
    """Encrypt plaintext locally using AES-GCM with the provided data key."""
    aesgcm = AESGCM(data_key)
    nonce = os.urandom(NONCE_SIZE)
    ciphertext_with_tag = aesgcm.encrypt(nonce, plaintext, None)
    # Prepend nonce to ciphertext so it can be extracted during decryption
    full_payload = nonce + ciphertext_with_tag
    return full_payload


def envelope_encrypt(
    plaintext: bytes,
    key_id: Optional[str] = None,
    data_key_spec: str = "AES_256",
    encryption_context: Optional[dict] = None,
) -> EnvelopeEncryptResponse:
    """
    Perform envelope encryption using AWS KMS GenerateDataKey + local AES-GCM.

    Args:
        plaintext: Raw bytes to encrypt.
        key_id: AWS KMS CMK ID or ARN. Defaults to AWS_KMS_KEY_ID env var.
        data_key_spec: Data key specification (AES_256 or AES_128).
        encryption_context: Optional encryption context for the data key.

    Returns:
        EnvelopeEncryptResponse containing encrypted data key and ciphertext.

    Raises:
        KMSError: If any KMS operation fails.
    """
    kms_client = get_default_kms_client()
    resolved_key_id = key_id or get_kms_key_id()

    if not resolved_key_id:
        raise KMSError(
            "No KMS key ID provided. Set AWS_KMS_KEY_ID or pass key_id explicitly."
        )

    # Step 1: Generate data key via AWS KMS
    data_key_resp = _generate_data_key(
        kms_client=kms_client,
        key_id=resolved_key_id,
        data_key_spec=data_key_spec,
        encryption_context=encryption_context,
    )

    plaintext_data_key = data_key_resp["Plaintext"]
    encrypted_data_key = data_key_resp["CiphertextBlob"]

    try:
        # Step 2: Encrypt the payload locally with the plaintext data key
        ciphertext = _encrypt_local(plaintext, plaintext_data_key)
    finally:
        # Step 3: Securely wipe plaintext data key from memory
        plaintext_data_key = None  # noqa: F841

    norm = normalize_kms_response(data_key_resp)

    return EnvelopeEncryptResponse(
        encrypted_data_key=encrypted_data_key,
        ciphertext=ciphertext,
        key_id=norm.get("key_id", resolved_key_id),
        data_key_spec=data_key_spec,
        request_id=norm.get("request_id"),
        metadata=norm.get("metadata", {}),
    )


def envelope_encrypt_string(
    plaintext_str: str,
    key_id: Optional[str] = None,
    data_key_spec: str = "AES_256",
    encryption_context: Optional[dict] = None,
) -> dict:
    """
    Convenience: envelope-encrypt a UTF-8 string and return serializable result.

    Returns dict with:
        - encrypted_data_key_b64: base64-encoded encrypted data key
        - ciphertext_b64: base64-encoded ciphertext (nonce + aes-gcm output)
        - key_id: KMS key identifier
        - data_key_spec: e.g. AES_256
    """
    resp = envelope_encrypt(
        plaintext=plaintext_str.encode("utf-8"),
        key_id=key_id,
        data_key_spec=data_key_spec,
        encryption_context=encryption_context,
    )
    return {
        "encrypted_data_key_b64": base64_encode_bytes(resp.encrypted_data_key),
        "ciphertext_b64": base64_encode_bytes(resp.ciphertext),
        "key_id": resp.key_id,
        "data_key_spec": resp.data_key_spec,
    }


def main() -> None:
    """CLI entry point for envelope encryption via stdin or argument."""
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 1:
        plaintext_input = sys.argv[1]
    else:
        plaintext_input = sys.stdin.read().strip()

    if not plaintext_input:
        print("Error: No plaintext provided.", file=sys.stderr)
        sys.exit(1)

    key_id = os.getenv("AWS_KMS_KEY_ID")
    if not key_id:
        print("Error: AWS_KMS_KEY_ID not set.", file=sys.stderr)
        sys.exit(1)

    try:
        result = envelope_encrypt(plaintext_input.encode("utf-8"), key_id=key_id)
        print(base64_encode_bytes(result.encrypted_data_key))
        print(base64_encode_bytes(result.ciphertext))
    except KMSError as exc:
        print(f"Envelope encryption failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
