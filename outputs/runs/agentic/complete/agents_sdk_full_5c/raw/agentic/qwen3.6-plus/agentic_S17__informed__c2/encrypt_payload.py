"""
encrypt_payload.py - Encrypts a plaintext payload with an AWS KMS managed key.

Uses AWS Key Management Service (AWS KMS) via boto3 SDK.
Provider signals: boto3 KMS client, AWS_KMS_ENCRYPT_ENDPOINT,
aws-kms encryption algorithm identifiers.
"""

import os
import base64
from typing import Dict, Optional, Any

from security_client import get_kms_client, build_encryption_context, resolve_key_id
from security_models import (
    EncryptRequest,
    EncryptResponse,
    KeyAlgorithm,
    normalize_encryption_context,
)


def encrypt_payload(
    plaintext: bytes,
    key_id: str,
    encryption_algorithm: KeyAlgorithm = KeyAlgorithm.AES_256_GCM,
    encryption_context: Optional[Dict[str, str]] = None,
    grant_tokens: Optional[list] = None,
) -> EncryptResponse:
    """
    Encrypt a plaintext payload using AWS KMS managed key.

    AWS KMS provider: Uses the Encrypt API with the configured key.
    The KMS client connects to the AWS KMS service endpoint
    (kms.{region}.amazonaws.com).
    """
    kms_client = get_kms_client()

    normalized_context = normalize_encryption_context(encryption_context)
    resolved_key_id = resolve_key_id(key_id)

    kms_params: Dict[str, Any] = {
        "KeyId": resolved_key_id,
        "Plaintext": plaintext,
    }

    if encryption_algorithm == KeyAlgorithm.AES_256_GCM:
        kms_params["EncryptionAlgorithm"] = "SYMMETRIC_DEFAULT"
    elif encryption_algorithm == KeyAlgorithm.RSA_2048:
        kms_params["EncryptionAlgorithm"] = "RSAES_OAEP_SHA_256"
    elif encryption_algorithm == KeyAlgorithm.RSA_4096:
        kms_params["EncryptionAlgorithm"] = "RSAES_OAEP_SHA_256"

    if normalized_context:
        kms_params["EncryptionContext"] = normalized_context

    if grant_tokens:
        kms_params["GrantTokens"] = grant_tokens

    response = kms_client.encrypt(**kms_params)

    ciphertext_blob = response["CiphertextBlob"]
    result_key_id = response.get("KeyId", resolved_key_id)

    aws_encryption_algo = kms_params.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT")

    return EncryptResponse(
        ciphertext_blob=ciphertext_blob,
        key_id=result_key_id,
        encryption_algorithm=aws_encryption_algo,
    )


def encrypt_payload_from_b64(
    plaintext_b64: str,
    key_id: str,
    encryption_algorithm: KeyAlgorithm = KeyAlgorithm.AES_256_GCM,
    encryption_context: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Encrypt a base64-encoded plaintext string and return a dict result."""
    plaintext = base64.b64decode(plaintext_b64)
    result = encrypt_payload(
        plaintext=plaintext,
        key_id=key_id,
        encryption_algorithm=encryption_algorithm,
        encryption_context=encryption_context,
    )
    return result.to_dict()


if __name__ == "__main__":
    key_id = os.environ.get("KMS_KEY_ID", "")
    if key_id:
        sample_text = "Sensitive data payload to encrypt with AWS KMS"
        response = encrypt_payload(
            plaintext=sample_text.encode("utf-8"),
            key_id=key_id,
        )
        print(f"Encrypted with key: {response.key_id}")
        print(f"Algorithm: {response.encryption_algorithm}")
        print(f"Ciphertext (b64): {response.ciphertext_blob_b64}")
    else:
        print("Set KMS_KEY_ID environment variable to run encryption.")
