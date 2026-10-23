"""
Encrypts a plaintext payload with a managed key using AWS KMS.
AWS Key Management Service (boto3) is the concrete provider for encryption.
"""

import os
import base64
import sys
from typing import Optional, Dict

from security_client import KMSClientHelper
from security_models import (
    EncryptionRequest,
    EncryptionResponse,
    normalize_encryption_context,
)


def encrypt_payload(
    key_id: str,
    plaintext: str,
    encryption_context: Optional[Dict[str, str]] = None,
    algorithm: str = "SYMMETRIC_DEFAULT",
    region: Optional[str] = None,
) -> EncryptionResponse:
    """
    Encrypt a plaintext payload using AWS KMS managed key.

    Uses AWS KMS Encrypt API with the specified key ID.
    The AWS KMS service is identified by boto3 kms client and AWS credentials.

    Args:
        key_id: AWS KMS key ID or ARN.
        plaintext: The plaintext string to encrypt.
        encryption_context: Optional context for additional authenticated data.
        algorithm: Encryption algorithm (default: SYMMETRIC_DEFAULT).
        region: AWS region override.

    Returns:
        EncryptionResponse containing ciphertext blob and metadata.

    Raises:
        ValueError: If key_id or plaintext is empty.
        KMSError: If AWS KMS encryption fails.
    """
    if not key_id:
        raise ValueError("key_id is required")
    if not plaintext:
        raise ValueError("plaintext is required")

    normalized_context = normalize_encryption_context(encryption_context)

    request = EncryptionRequest(
        key_id=key_id,
        plaintext=plaintext,
        encryption_context=normalized_context,
        algorithm=algorithm,
    )

    kms_helper = KMSClientHelper(region=region)
    response = kms_helper.encrypt(
        key_id=request.key_id,
        plaintext=request.plaintext,
        encryption_context=request.encryption_context,
        algorithm=request.algorithm,
    )

    return response


def main():
    """CLI entry point for encrypt_payload."""
    key_id = os.environ.get("KMS_KEY_ID")
    plaintext = os.environ.get("PLAINTEXT", "default-payload-to-encrypt")

    if not key_id:
        print("Error: KMS_KEY_ID environment variable is required")
        sys.exit(1)

    encryption_context_str = os.environ.get("ENCRYPTION_CONTEXT")
    encryption_context = None
    if encryption_context_str:
        import json
        encryption_context = json.loads(encryption_context_str)

    try:
        response = encrypt_payload(
            key_id=key_id,
            plaintext=plaintext,
            encryption_context=encryption_context,
        )
        print(f"Key ID: {response.key_id}")
        print(f"Algorithm: {response.encryption_algorithm}")
        print(f"Ciphertext (base64): {response.to_base64()}")
    except Exception as e:
        print(f"Encryption failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
