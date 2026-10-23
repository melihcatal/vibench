"""
Implements envelope encryption using AWS KMS managed key service.
Generates a data key via AWS KMS GenerateDataKey, encrypts the payload
locally with the plaintext data key (AES-256-GCM via cryptography),
and returns the encrypted data key alongside the encrypted payload.
"""

import json
import os
import base64
import logging
from typing import Optional, Dict

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend

from security_client import create_kms_client, get_default_key_id, handle_kms_error, build_encryption_context
from security_models import (
    EnvelopeEncryptionRequest,
    EnvelopeEncryptionResponse,
    normalize_encryption_context,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# AWS KMS data key spec constants
AWS_KMS_DATA_KEY_SPEC_256 = "AES_256"
AWS_KMS_DATA_KEY_SPEC_128 = "AES_128"


def generate_data_key_kms(key_id: str, key_spec: str = AWS_KMS_DATA_KEY_SPEC_256,
                          encryption_context: Optional[Dict[str, str]] = None) -> Dict:
    """
    Generate a data key using AWS KMS GenerateDataKey API.

    Provider: AWS KMS (boto3) - kms.us-east-1.amazonaws.com
    Key spec: AES_256 for 256-bit data key generation.

    Args:
        key_id: The KMS key ID or ARN used to encrypt the data key.
        key_spec: Key specification (AES_256 or AES_128).
        encryption_context: Optional encryption context.

    Returns:
        Dict with Plaintext (bytes), CiphertextBlob (bytes), KeyId, ResponseMetadata.
    """
    kms_client = create_kms_client()
    normalized_context = normalize_encryption_context(encryption_context)

    params = {
        "KeyId": key_id,
        "KeySpec": key_spec,
    }
    if normalized_context:
        params["EncryptionContext"] = normalized_context

    logger.info("Generating data key with AWS KMS key %s, spec %s", key_id, key_spec)
    response = kms_client.generate_data_key(**params)
    return response


def encrypt_with_aes_gcm(plaintext: bytes, data_key: bytes, aad: Optional[bytes] = None) -> bytes:
    """
    Encrypt plaintext using AES-256-GCM with the provided data key.

    Args:
        plaintext: Data to encrypt.
        data_key: Plaintext data key from KMS.
        aad: Optional additional authenticated data.

    Returns:
        Nonce + ciphertext + tag bytes.
    """
    aesgcm = AESGCM(data_key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plaintext, aad)
    return nonce + ct


def decrypt_with_aes_gcm(ciphertext: bytes, data_key: bytes, aad: Optional[bytes] = None) -> bytes:
    """
    Decrypt ciphertext using AES-256-GCM with the provided data key.

    Args:
        ciphertext: Nonce + ciphertext + tag bytes.
        data_key: Plaintext data key from KMS.
        aad: Optional additional authenticated data.

    Returns:
        Decrypted plaintext bytes.
    """
    aesgcm = AESGCM(data_key)
    nonce = ciphertext[:12]
    ct_with_tag = ciphertext[12:]
    return aesgcm.decrypt(nonce, ct_with_tag, aad)


def envelope_encrypt(
    plaintext: str,
    key_id: str = "",
    encryption_context: Optional[Dict[str, str]] = None,
    data_key_length: int = 32,
) -> EnvelopeEncryptionResponse:
    """
    Perform envelope encryption using AWS KMS.

    1. Generate a data key via AWS KMS GenerateDataKey (AES_256).
    2. Encrypt the plaintext with the data key using AES-256-GCM.
    3. Return the encrypted data key and encrypted payload.

    Provider: AWS KMS (boto3) - kms.us-east-1.amazonaws.com
    Algorithm: AES_256 for data key, AES-256-GCM for payload.

    Args:
        plaintext: The plaintext to encrypt.
        key_id: The AWS KMS key ID to use for data key generation.
        encryption_context: Optional encryption context.
        data_key_length: Expected data key length in bytes.

    Returns:
        EnvelopeEncryptionResponse with encrypted_data_key and encrypted_payload.
    """
    request = EnvelopeEncryptionRequest(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=encryption_context or {},
        data_key_length=data_key_length,
    )

    if not request.key_id:
        request.key_id = get_default_key_id()

    # Step 1: Generate data key via AWS KMS
    dk_response = generate_data_key_kms(
        key_id=request.key_id,
        key_spec=AWS_KMS_DATA_KEY_SPEC_256,
        encryption_context=request.encryption_context,
    )

    plaintext_data_key = dk_response["Plaintext"]
    encrypted_data_key = dk_response["CiphertextBlob"]
    kms_key_id = dk_response["KeyId"]

    # Step 2: Encrypt payload with data key using AES-256-GCM
    payload_bytes = request.to_normalized_payload()
    encrypted_payload = encrypt_with_aes_gcm(payload_bytes, plaintext_data_key)

    # Build response
    result = EnvelopeEncryptionResponse(
        encrypted_data_key=base64.b64encode(encrypted_data_key).decode("utf-8"),
        encrypted_payload=base64.b64encode(encrypted_payload).decode("utf-8"),
        key_id=kms_key_id,
        encryption_context=normalize_encryption_context(request.encryption_context),
        algorithm="AES_256_GCM",
        request_id=dk_response.get("ResponseMetadata", {}).get("RequestId", ""),
    )

    logger.info("Envelope encryption completed with AWS KMS key %s", kms_key_id)
    return result


def envelope_decrypt(
    encrypted_data_key: str,
    encrypted_payload: str,
    encryption_context: Optional[Dict[str, str]] = None,
) -> str:
    """
    Decrypt envelope-encrypted data using AWS KMS.

    1. Decrypt the data key via AWS KMS Decrypt.
    2. Use the decrypted data key to decrypt the payload with AES-256-GCM.

    Args:
        encrypted_data_key: Base64-encoded encrypted data key.
        encrypted_payload: Base64-encoded encrypted payload (nonce + ct + tag).
        encryption_context: Optional encryption context.

    Returns:
        Decrypted plaintext string.
    """
    kms_client = create_kms_client()
    normalized_context = normalize_encryption_context(encryption_context)

    data_key_blob = base64.b64decode(encrypted_data_key)
    payload_bytes = base64.b64decode(encrypted_payload)

    decrypt_params = {"CiphertextBlob": data_key_blob}
    if normalized_context:
        decrypt_params["EncryptionContext"] = normalized_context

    dk_response = kms_client.decrypt(**decrypt_params)
    plaintext_data_key = dk_response["Plaintext"]

    plaintext_bytes = decrypt_with_aes_gcm(payload_bytes, plaintext_data_key)
    return plaintext_bytes.decode("utf-8", errors="replace")


if __name__ == "__main__":
    sample = "Sensitive data for envelope encryption with AWS KMS."
    result = envelope_encrypt(sample)
    print(result.to_json())
