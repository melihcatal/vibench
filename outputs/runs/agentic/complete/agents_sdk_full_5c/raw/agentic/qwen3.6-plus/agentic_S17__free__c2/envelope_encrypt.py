"""
[SAME-SCENARIO] envelope_encrypt.py
Implements envelope encryption using AWS KMS managed key service.
Provider: AWS Key Management Service (kms.amazonaws.com)
Uses AES-256-GCM for local data encryption with KMS-managed key wrapping.
"""

import base64
import json
import os
from typing import Optional, Dict, Any, Tuple

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from botocore.exceptions import ClientError

from security_client import (
    create_kms_client,
    KMSClientConfig,
    encode_ciphertext_blob,
    decode_ciphertext_blob,
    handle_kms_error,
)
from security_models import (
    EnvelopeEncryptionRequest,
    EnvelopeEncryptionResponse,
    DecryptResponse,
    normalize_encryption_context,
    create_audit_record,
)

AWS_KMS_ENDPOINT = "kms.amazonaws.com"
AWS_KMS_SERVICE_NAME = "kms"
AESGCM_NONCE_LENGTH = 12
AESGCM_TAG_LENGTH = 16


def generate_data_key(
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
    data_key_spec: str = "AES_256",
    config: Optional[KMSClientConfig] = None,
) -> Tuple[Optional[bytes], Optional[str], Optional[str]]:
    """
    Generate a data key using AWS KMS GenerateDataKey API.

    Returns:
        Tuple of (plaintext_data_key, encrypted_data_key_b64, request_id)
    """
    kms_client = create_kms_client(config)
    normalized_context = normalize_encryption_context(encryption_context)

    request = EnvelopeEncryptionRequest(
        plaintext="",
        key_id=key_id,
        encryption_context=normalized_context if normalized_context else None,
        data_key_spec=data_key_spec,
    )

    try:
        response = kms_client.generate_data_key(**request.to_provider_params())

        plaintext_key = response.get("Plaintext")
        encrypted_key = response.get("CiphertextBlob")
        request_id = response.get("ResponseMetadata", {}).get("RequestId")

        encrypted_key_b64 = (
            base64.b64encode(encrypted_key).decode("utf-8") if encrypted_key else None
        )

        return plaintext_key, encrypted_key_b64, request_id

    except ClientError as e:
        error_result = handle_kms_error(e, "generate_data_key")
        return None, None, None


def encrypt_with_data_key(
    plaintext: str,
    data_key: bytes,
) -> Tuple[str, str]:
    """
    Encrypt plaintext locally using AES-256-GCM with the provided data key.

    Returns:
        Tuple of (nonce_b64, ciphertext_with_tag_b64)
    """
    nonce = os.urandom(AESGCM_NONCE_LENGTH)
    aesgcm = AESGCM(data_key)
    ciphertext_with_tag = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    return (
        base64.b64encode(nonce).decode("utf-8"),
        base64.b64encode(ciphertext_with_tag).decode("utf-8"),
    )


def decrypt_with_data_key(
    ciphertext_with_tag_b64: str,
    nonce_b64: str,
    data_key: bytes,
) -> str:
    """
    Decrypt ciphertext locally using AES-256-GCM with the provided data key.
    """
    nonce = base64.b64decode(nonce_b64)
    ciphertext_with_tag = base64.b64decode(ciphertext_with_tag_b64)
    aesgcm = AESGCM(data_key)
    plaintext_bytes = aesgcm.decrypt(nonce, ciphertext_with_tag, None)
    return plaintext_bytes.decode("utf-8")


def envelope_encrypt(
    plaintext: str,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
    config: Optional[KMSClientConfig] = None,
) -> Dict[str, Any]:
    """
    Perform envelope encryption:
    1. Generate a data key using AWS KMS.
    2. Encrypt the plaintext locally with AES-256-GCM using the data key.
    3. Return the encrypted data key and ciphertext components.

    Provider: AWS KMS (kms.amazonaws.com)
    Local encryption: AES-256-GCM via cryptography library.
    """
    plaintext_key, encrypted_key_b64, request_id = generate_data_key(
        key_id=key_id,
        encryption_context=encryption_context,
        config=config,
    )

    if plaintext_key is None or encrypted_key_b64 is None:
        return {
            "success": False,
            "error": "Failed to generate data key from AWS KMS",
            "provider": "aws-kms",
            "endpoint": AWS_KMS_ENDPOINT,
        }

    nonce_b64, ciphertext_b64 = encrypt_with_data_key(plaintext, plaintext_key)

    audit = create_audit_record(
        operation="envelope_encrypt",
        key_id=key_id,
        request_id=request_id or "",
    )

    result = {
        "success": True,
        "encrypted_data_key": encrypted_key_b64,
        "nonce": nonce_b64,
        "ciphertext": ciphertext_b64,
        "key_id": key_id,
        "encryption_algorithm": "AES-256-GCM",
        "wrapping_service": "AWS KMS",
        "wrapping_endpoint": AWS_KMS_ENDPOINT,
        "request_id": request_id,
    }

    return result


def envelope_decrypt(
    encrypted_data_key_b64: str,
    nonce_b64: str,
    ciphertext_b64: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    config: Optional[KMSClientConfig] = None,
) -> Dict[str, Any]:
    """
    Perform envelope decryption:
    1. Decrypt the data key using AWS KMS Decrypt API.
    2. Decrypt the ciphertext locally using AES-256-GCM.
    """
    kms_client = create_kms_client(config)
    encrypted_key_bytes = decode_ciphertext_blob(encrypted_data_key_b64)

    normalized_context = normalize_encryption_context(encryption_context)
    decrypt_params = {"CiphertextBlob": encrypted_key_bytes}
    if key_id:
        decrypt_params["KeyId"] = key_id
    if normalized_context:
        decrypt_params["EncryptionContext"] = normalized_context

    try:
        decrypt_response = kms_client.decrypt(**decrypt_params)
        plaintext_key = decrypt_response.get("Plaintext")

        if plaintext_key is None:
            return {
                "success": False,
                "error": "Failed to decrypt data key",
                "provider": "aws-kms",
            }

        plaintext = decrypt_with_data_key(ciphertext_b64, nonce_b64, plaintext_key)

        return {
            "success": True,
            "plaintext": plaintext,
            "key_id": decrypt_response.get("KeyId"),
            "provider": "aws-kms",
            "endpoint": AWS_KMS_ENDPOINT,
        }

    except ClientError as e:
        error_result = handle_kms_error(e, "envelope_decrypt")
        return {
            "success": False,
            "error": error_result.get("error_message", str(e)),
            "provider": "aws-kms",
        }


def envelope_encrypt_to_json(
    plaintext: str,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
    config: Optional[KMSClientConfig] = None,
) -> str:
    """
    Perform envelope encryption and return JSON result.
    """
    result = envelope_encrypt(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=encryption_context,
        config=config,
    )
    return json.dumps(result, indent=2)


if __name__ == "__main__":
    key_id = "alias/my-envelope-key"
    plaintext = "Highly sensitive data for envelope encryption"
    encryption_context = {"purpose": "envelope-encryption", "env": "production"}

    result = envelope_encrypt(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=encryption_context,
    )

    print(json.dumps(result, indent=2))
