"""
Implements envelope encryption using AWS KMS managed keys.

Uses the AWS KMS GenerateDataKey API (kms.amazonaws.com) with the boto3 SDK
to perform envelope encryption: a data key encrypts the payload locally
while the data key itself is encrypted by AWS KMS.

Algorithm: AES-256-GCM for local payload encryption.
"""

import os
import logging
from typing import Optional, Dict, Any

import boto3
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import get_kms_client, validate_key_id, build_encryption_context
from security_models import (
    EnvelopeEncryptionRequest,
    EnvelopeEncryptionResponse,
    EnvelopeDecryptionRequest,
    normalize_base64,
    denormalize_base64,
    normalize_key_id,
)

logger = logging.getLogger(__name__)


def envelope_encrypt(
    plaintext: str,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
    grant_tokens: Optional[list] = None,
    client=None,
) -> EnvelopeEncryptionResponse:
    """
    Perform envelope encryption using AWS KMS GenerateDataKey.

    Provider: AWS KMS (kms.amazonaws.com)
    API: kms.generate_data_key
    Local Algorithm: AES-256-GCM (cryptography library)

    Steps:
        1. Call AWS KMS GenerateDataKey to get a plaintext + encrypted data key pair.
        2. Use the plaintext data key to encrypt the payload with AES-256-GCM.
        3. Return the encrypted payload alongside the encrypted data key.

    Args:
        plaintext: The plaintext string to encrypt.
        key_id: AWS KMS CMK ID or ARN for wrapping the data key.
        encryption_context: Optional KMS encryption context.
        grant_tokens: Optional grant tokens.
        client: Optional pre-initialized boto3 KMS client.

    Returns:
        EnvelopeEncryptionResponse with encrypted data key and encrypted payload.

    Raises:
        ValueError: If key_id is invalid.
        Exception: On KMS API or cryptographic failure.
    """
    if not validate_key_id(key_id):
        raise ValueError(f"Invalid AWS KMS key identifier: {key_id}")

    if client is None:
        client = get_kms_client()

    normalized_key = normalize_key_id(key_id)

    generate_params = {
        "KeyId": normalized_key,
        "KeySpec": "AES_256",
    }

    if encryption_context:
        generate_params["EncryptionContext"] = encryption_context
    else:
        generate_params["EncryptionContext"] = build_encryption_context(
            {"operation": "envelope-encrypt"}
        )

    if grant_tokens:
        generate_params["GrantTokens"] = grant_tokens

    logger.info(
        "Calling AWS KMS GenerateDataKey for key %s (region: %s)",
        normalized_key,
        os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    )

    generate_response = client.generate_data_key(**generate_params)

    plaintext_data_key = generate_response["Plaintext"]
    encrypted_data_key = generate_response["CiphertextBlob"]

    try:
        aesgcm = AESGCM(plaintext_data_key)
        nonce = os.urandom(12)
        plaintext_bytes = plaintext.encode("utf-8")
        encrypted_payload_bytes = nonce + aesgcm.encrypt(nonce, plaintext_bytes, None)
    finally:
        # Wipe plaintext data key from memory after use
        plaintext_data_key = b"\x00" * len(plaintext_data_key)

    result = EnvelopeEncryptionResponse(
        encrypted_data_key=normalize_base64(encrypted_data_key),
        encrypted_payload=normalize_base64(encrypted_payload_bytes),
        key_id=generate_response.get("KeyId", normalized_key),
        algorithm="AES-256-GCM",
    )

    logger.info(
        "Envelope encryption succeeded with AWS KMS key %s",
        result.key_id,
    )

    return result


def envelope_decrypt(
    encrypted_data_key: str,
    encrypted_payload: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    grant_tokens: Optional[list] = None,
    client=None,
) -> str:
    """
    Perform envelope decryption using AWS KMS Decrypt on the data key.

    Provider: AWS KMS (kms.amazonaws.com)
    API: kms.decrypt (for the data key)
    Local Algorithm: AES-256-GCM (cryptography library)

    Args:
        encrypted_data_key: Base64-encoded encrypted data key from envelope encrypt.
        encrypted_payload: Base64-encoded encrypted payload.
        key_id: Optional KMS key ID constraint for decryption.
        encryption_context: Optional KMS encryption context.
        grant_tokens: Optional grant tokens.
        client: Optional pre-initialized boto3 KMS client.

    Returns:
        Decrypted plaintext string.

    Raises:
        Exception: On KMS API or cryptographic failure.
    """
    if client is None:
        client = get_kms_client()

    encrypted_data_key_bytes = denormalize_base64(encrypted_data_key)

    decrypt_params = {
        "CiphertextBlob": encrypted_data_key_bytes,
        "EncryptionAlgorithm": "SYMMETRIC_DEFAULT",
    }

    if key_id:
        decrypt_params["KeyId"] = normalize_key_id(key_id)

    if encryption_context:
        decrypt_params["EncryptionContext"] = encryption_context
    else:
        decrypt_params["EncryptionContext"] = build_encryption_context(
            {"operation": "envelope-encrypt"}
        )

    if grant_tokens:
        decrypt_params["GrantTokens"] = grant_tokens

    logger.info("Calling AWS KMS Decrypt for data key recovery")

    decrypt_response = client.decrypt(**decrypt_params)
    plaintext_data_key = decrypt_response["Plaintext"]

    try:
        encrypted_payload_bytes = denormalize_base64(encrypted_payload)
        nonce = encrypted_payload_bytes[:12]
        ciphertext = encrypted_payload_bytes[12:]
        aesgcm = AESGCM(plaintext_data_key)
        decrypted_bytes = aesgcm.decrypt(nonce, ciphertext, None)
        return decrypted_bytes.decode("utf-8")
    finally:
        plaintext_data_key = b"\x00" * len(plaintext_data_key)


def envelope_encrypt_from_request(
    request: EnvelopeEncryptionRequest, client=None
) -> EnvelopeEncryptionResponse:
    """
    Envelope encrypt using an EnvelopeEncryptionRequest dataclass.

    Args:
        request: EnvelopeEncryptionRequest with all required parameters.
        client: Optional pre-initialized boto3 KMS client.

    Returns:
        EnvelopeEncryptionResponse with encrypted data.
    """
    return envelope_encrypt(
        plaintext=request.plaintext,
        key_id=request.key_id,
        encryption_context=request.encryption_context,
        client=client,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sample_key = os.environ.get("AWS_KMS_ENVELOPE_KEY_ID", "")
    if sample_key:
        result = envelope_encrypt("Sensitive envelope data", sample_key)
        print(f"Key ID: {result.key_id}")
        print(f"Encrypted Data Key: {result.encrypted_data_key[:40]}...")
        print(f"Encrypted Payload: {result.encrypted_payload[:40]}...")

        decrypted = envelope_decrypt(
            result.encrypted_data_key, result.encrypted_payload, sample_key
        )
        print(f"Decrypted: {decrypted}")
    else:
        print("Set AWS_KMS_ENVELOPE_KEY_ID environment variable to test.")
