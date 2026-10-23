"""
envelope_encrypt.py - Implements envelope encryption using AWS KMS.

Provider: AWS Key Management Service (KMS)
Service endpoint: kms.{region}.amazonaws.com
Concrete model: AWS KMS GenerateDataKey (AES_256 data keys) + local AES-GCM
"""

from __future__ import annotations

import os
from typing import Dict, Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import (
    SecurityClientConfig,
    create_kms_client,
    handle_kms_error,
    extract_key_arn_from_response,
)
from security_models import (
    EnvelopeEncryptRequest,
    EnvelopeEncryptResponse,
    encode_bytes,
    decode_bytes,
    normalize_key_id,
)

DATA_KEY_SPEC_MAP = {
    "AES_256": "AES_256",
    "AES_128": "AES_128",
}


def generate_data_key(
    key_id: str,
    data_key_spec: str = "AES_256",
    encryption_context: Optional[Dict[str, str]] = None,
    config: Optional[SecurityClientConfig] = None,
) -> dict:
    """
    Generate a data key using AWS KMS GenerateDataKey API.

    AWS KMS returns both the plaintext data key and the encrypted data key.
    The plaintext key is used for local encryption; the encrypted key is stored.
    """
    kms_client = create_kms_client(config)

    spec = DATA_KEY_SPEC_MAP.get(data_key_spec, "AES_256")

    generate_kwargs = {
        "KeyId": normalize_key_id(key_id),
        "KeySpec": spec,
    }

    if encryption_context:
        generate_kwargs["EncryptionContext"] = encryption_context

    try:
        response = kms_client.generate_data_key(**generate_kwargs)
    except Exception as e:
        handle_kms_error(e, context="envelope_encrypt:generate_data_key")

    return {
        "plaintext_key": response["Plaintext"],
        "encrypted_key": response["CiphertextBlob"],
        "key_id": extract_key_arn_from_response(response, key_id),
        "key_spec": spec,
    }


def encrypt_data_locally(
    plaintext: str,
    data_key: bytes,
    encryption_context: Optional[Dict[str, str]] = None,
) -> tuple:
    """
    Encrypt plaintext locally using AES-GCM with the data key.

    Uses the cryptography library's AESGCM implementation with
    a random nonce. Returns ciphertext and nonce.
    """
    aesgcm = AESGCM(data_key)
    nonce = os.urandom(12)

    associated_data = b""
    if encryption_context:
        associated_data = "|".join(
            f"{k}={v}" for k, v in sorted(encryption_context.items())
        ).encode("utf-8")

    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), associated_data)
    return ciphertext, nonce


def envelope_encrypt(
    plaintext: str,
    key_id: str,
    data_key_spec: str = "AES_256",
    encryption_context: Optional[Dict[str, str]] = None,
    config: Optional[SecurityClientConfig] = None,
) -> EnvelopeEncryptResponse:
    """
    Perform envelope encryption using AWS KMS.

    Flow:
    1. Call AWS KMS GenerateDataKey to get a plaintext + encrypted data key pair.
    2. Use the plaintext data key to encrypt the payload locally via AES-GCM.
    3. Return the encrypted data key and encrypted payload (base64-encoded).

    The encrypted data key can later be decrypted via AWS KMS Decrypt API
    to recover the plaintext data key for decryption.

    Args:
        plaintext: The data to encrypt.
        key_id: AWS KMS CMK ID or ARN.
        data_key_spec: "AES_256" or "AES_128".
        encryption_context: Optional context for KMS and local binding.
        config: Optional SecurityClientConfig.

    Returns:
        EnvelopeEncryptResponse with encrypted data key and encrypted payload.
    """
    data_key_result = generate_data_key(
        key_id=key_id,
        data_key_spec=data_key_spec,
        encryption_context=encryption_context,
        config=config,
    )

    plaintext_data_key = data_key_result["plaintext_key"]
    encrypted_data_key = data_key_result["encrypted_key"]

    ciphertext, nonce = encrypt_data_locally(
        plaintext, plaintext_data_key, encryption_context
    )

    combined_payload = nonce + ciphertext

    return EnvelopeEncryptResponse(
        encrypted_data_key=encode_bytes(encrypted_data_key),
        encrypted_payload=encode_bytes(combined_payload),
        plaintext_data_key=encode_bytes(plaintext_data_key),
    )


def decrypt_envelope_payload(
    encrypted_data_key: str,
    encrypted_payload: str,
    encryption_context: Optional[Dict[str, str]] = None,
    config: Optional[SecurityClientConfig] = None,
) -> str:
    """
    Decrypt an envelope-encrypted payload.

    Flow:
    1. Decrypt the encrypted data key using AWS KMS Decrypt.
    2. Use the recovered plaintext data key to decrypt the payload via AES-GCM.

    Args:
        encrypted_data_key: Base64-encoded encrypted data key from KMS.
        encrypted_payload: Base64-encoded (nonce + ciphertext).
        encryption_context: Must match the context used during encryption.
        config: Optional SecurityClientConfig.

    Returns:
        Decrypted plaintext string.
    """
    kms_client = create_kms_client(config)

    encrypted_key_bytes = decode_bytes(encrypted_data_key)

    decrypt_kwargs = {
        "CiphertextBlob": encrypted_key_bytes,
        "EncryptionAlgorithm": "SYMMETRIC_DEFAULT",
    }

    if encryption_context:
        decrypt_kwargs["EncryptionContext"] = encryption_context

    try:
        response = kms_client.decrypt(**decrypt_kwargs)
    except Exception as e:
        handle_kms_error(e, context="envelope_decrypt:decrypt_data_key")

    plaintext_data_key = response["Plaintext"]

    payload_bytes = decode_bytes(encrypted_payload)
    nonce = payload_bytes[:12]
    ciphertext = payload_bytes[12:]

    aesgcm = AESGCM(plaintext_data_key)

    associated_data = b""
    if encryption_context:
        associated_data = "|".join(
            f"{k}={v}" for k, v in sorted(encryption_context.items())
        ).encode("utf-8")

    decrypted = aesgcm.decrypt(nonce, ciphertext, associated_data)
    return decrypted.decode("utf-8")


def envelope_encrypt_from_request(
    request: EnvelopeEncryptRequest,
    config: Optional[SecurityClientConfig] = None,
) -> EnvelopeEncryptResponse:
    """Perform envelope encryption from a normalized request."""
    return envelope_encrypt(
        plaintext=request.plaintext,
        key_id=request.key_id,
        data_key_spec=request.data_key_spec,
        encryption_context=request.encryption_context,
        config=config,
    )


if __name__ == "__main__":
    key_id = os.environ.get("KMS_KEY_ID", "alias/default")
    plaintext = os.environ.get("PLAINTEXT", "confidential-envelope-data")

    response = envelope_encrypt(plaintext, key_id)
    print(f"Encrypted data key (first 40 chars): {response.encrypted_data_key[:40]}...")
    print(f"Encrypted payload (first 40 chars): {response.encrypted_payload[:40]}...")

    decrypted = decrypt_envelope_payload(
        response.encrypted_data_key, response.encrypted_payload
    )
    print(f"Decrypted: {decrypted}")
