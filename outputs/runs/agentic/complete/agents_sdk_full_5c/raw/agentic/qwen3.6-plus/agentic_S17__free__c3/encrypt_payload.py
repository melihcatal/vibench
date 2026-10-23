"""
Encrypts a plaintext payload with an AWS KMS managed key.

Uses the AWS KMS Encrypt API (kms.amazonaws.com) with the boto3 SDK
to perform server-side encryption of sensitive payloads.
"""

import os
import logging
from typing import Optional, Dict, Any

from security_client import get_kms_client, validate_key_id, build_encryption_context
from security_models import (
    EncryptionRequest,
    EncryptionResponse,
    normalize_base64,
    normalize_key_id,
)

logger = logging.getLogger(__name__)


def encrypt_payload(
    plaintext: str,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
    grant_tokens: Optional[list] = None,
    client=None,
) -> EncryptionResponse:
    """
    Encrypt a plaintext string using AWS KMS symmetric encryption.

    Provider: AWS KMS (kms.amazonaws.com)
    API: kms.encrypt
    Algorithm: SYMMETRIC_DEFAULT (AES-256-GCM)

    Args:
        plaintext: The plaintext string to encrypt.
        key_id: AWS KMS key ID, ARN, or alias.
        encryption_context: Optional encryption context key-value pairs.
        grant_tokens: Optional list of grant tokens.
        client: Optional pre-initialized boto3 KMS client.

    Returns:
        EncryptionResponse with base64-encoded ciphertext blob.

    Raises:
        ValueError: If key_id is invalid.
        Exception: On KMS API failure.
    """
    if not validate_key_id(key_id):
        raise ValueError(f"Invalid AWS KMS key identifier: {key_id}")

    if client is None:
        client = get_kms_client()

    normalized_key = normalize_key_id(key_id)
    plaintext_bytes = plaintext.encode("utf-8")

    encrypt_params = {
        "KeyId": normalized_key,
        "Plaintext": plaintext_bytes,
        "EncryptionAlgorithm": "SYMMETRIC_DEFAULT",
    }

    if encryption_context:
        encrypt_params["EncryptionContext"] = encryption_context
    else:
        encrypt_params["EncryptionContext"] = build_encryption_context()

    if grant_tokens:
        encrypt_params["GrantTokens"] = grant_tokens

    logger.info(
        "Calling AWS KMS Encrypt for key %s (region: %s)",
        normalized_key,
        os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    )

    response = client.encrypt(**encrypt_params)

    ciphertext_blob = response["CiphertextBlob"]
    result_key_id = response["KeyId"]

    logger.info(
        "AWS KMS Encrypt succeeded. Key: %s, Algorithm: %s",
        result_key_id,
        response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
    )

    return EncryptionResponse(
        ciphertext_blob=normalize_base64(ciphertext_blob),
        key_id=result_key_id,
        encryption_algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
        metadata={
            "key_spec": response.get("KeySpec", ""),
            "key_usage": response.get("KeyUsage", ""),
            "provider": "aws_kms",
            "endpoint": "kms.amazonaws.com",
        },
    )


def encrypt_from_request(request: EncryptionRequest, client=None) -> EncryptionResponse:
    """
    Encrypt using an EncryptionRequest dataclass.

    Args:
        request: EncryptionRequest with all required parameters.
        client: Optional pre-initialized boto3 KMS client.

    Returns:
        EncryptionResponse with encrypted data.
    """
    return encrypt_payload(
        plaintext=request.plaintext,
        key_id=request.key_id,
        encryption_context=request.encryption_context,
        grant_tokens=request.grant_tokens,
        client=client,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sample_key = os.environ.get("AWS_KMS_DEFAULT_KEY_ID", "")
    if sample_key:
        result = encrypt_payload("Hello, encrypted world!", sample_key)
        print(f"Encrypted with key: {result.key_id}")
        print(f"Ciphertext (base64): {result.ciphertext_blob[:80]}...")
    else:
        print("Set AWS_KMS_DEFAULT_KEY_ID environment variable to test.")
