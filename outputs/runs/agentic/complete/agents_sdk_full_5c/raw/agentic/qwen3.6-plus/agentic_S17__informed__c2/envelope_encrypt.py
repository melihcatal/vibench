"""
envelope_encrypt.py - Implements envelope encryption using AWS KMS managed key.

Uses AWS Key Management Service (AWS KMS) via boto3 SDK.
Provider signals: boto3 KMS client, aws-kms GenerateDataKey API,
AWS_KMS_GENERATE_DATAKEY_ENDPOINT.
"""

import os
import base64
from typing import Dict, Optional, Any

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from security_client import (
    get_kms_client,
    build_encryption_context,
    resolve_key_id,
)
from security_models import (
    EnvelopeEncryptRequest,
    EnvelopeEncryptResponse,
    normalize_encryption_context,
)


def envelope_encrypt(
    plaintext: bytes,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
    data_key_spec: str = "AES_256",
) -> EnvelopeEncryptResponse:
    """
    Perform envelope encryption using AWS KMS GenerateDataKey API.

    AWS KMS provider: Uses GenerateDataKey to obtain a plaintext data key
    and an encrypted (wrapped) copy. The plaintext data key is used with
    AES-GCM locally to encrypt the payload. The encrypted data key is
    stored alongside the ciphertext so it can be unwrapped later.

    AWS KMS endpoint: kms.{region}.amazonaws.com
    """
    kms_client = get_kms_client()

    normalized_context = normalize_encryption_context(encryption_context)
    resolved_key_id = resolve_key_id(key_id)

    kms_params: Dict[str, Any] = {
        "KeyId": resolved_key_id,
        "KeySpec": data_key_spec,
    }

    if normalized_context:
        kms_params["EncryptionContext"] = normalized_context

    data_key_response = kms_client.generate_data_key(**kms_params)

    plaintext_data_key = data_key_response["Plaintext"]
    encrypted_data_key = data_key_response["CiphertextBlob"]

    aesgcm = AESGCM(plaintext_data_key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    result_encrypted_data_key = encrypted_data_key
    result_ciphertext = nonce + ciphertext
    result_key_id = data_key_response.get("KeyId", resolved_key_id)

    return EnvelopeEncryptResponse(
        encrypted_data_key=result_encrypted_data_key,
        ciphertext_blob=result_ciphertext,
        key_id=result_key_id,
    )


def envelope_decrypt(
    encrypted_data_key: bytes,
    ciphertext_blob: bytes,
    encryption_context: Optional[Dict[str, str]] = None,
) -> bytes:
    """
    Decrypt data encrypted with envelope_encrypt using AWS KMS.

    AWS KMS provider: Uses Decrypt API to unwrap the encrypted data key,
    then uses AES-GCM locally to decrypt the ciphertext.
    """
    kms_client = get_kms_client()

    normalized_context = normalize_encryption_context(encryption_context)

    kms_params: Dict[str, Any] = {
        "CiphertextBlob": encrypted_data_key,
    }

    if normalized_context:
        kms_params["EncryptionContext"] = normalized_context

    decrypt_response = kms_client.decrypt(**kms_params)
    plaintext_data_key = decrypt_response["Plaintext"]

    nonce = ciphertext_blob[:12]
    ciphertext = ciphertext_blob[12:]

    aesgcm = AESGCM(plaintext_data_key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)

    return plaintext


def envelope_encrypt_from_b64(
    plaintext_b64: str,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
    data_key_spec: str = "AES_256",
) -> Dict[str, Any]:
    """Encrypt a base64-encoded payload using envelope encryption."""
    plaintext = base64.b64decode(plaintext_b64)
    result = envelope_encrypt(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=encryption_context,
        data_key_spec=data_key_spec,
    )
    return result.to_dict()


if __name__ == "__main__":
    key_id = os.environ.get("KMS_KEY_ID", "")
    if key_id:
        sample_text = "Envelope-encrypted payload with AWS KMS data key"
        response = envelope_encrypt(
            plaintext=sample_text.encode("utf-8"),
            key_id=key_id,
        )
        print(f"Envelope encrypted with key: {response.key_id}")
        print(f"Encrypted data key (b64): {response.encrypted_data_key_b64}")
        print(f"Ciphertext (b64): {response.ciphertext_blob_b64}")

        decrypted = envelope_decrypt(
            encrypted_data_key=response.encrypted_data_key,
            ciphertext_blob=response.ciphertext_blob,
        )
        print(f"Decrypted: {decrypted.decode('utf-8')}")
    else:
        print("Set KMS_KEY_ID environment variable to run envelope encryption.")
