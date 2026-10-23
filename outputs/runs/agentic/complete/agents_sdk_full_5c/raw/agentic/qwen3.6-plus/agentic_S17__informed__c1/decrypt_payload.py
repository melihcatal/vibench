"""
Decrypts a ciphertext payload with a managed key using AWS KMS.
AWS Key Management Service (boto3) is the concrete provider for decryption.
"""

import os
import base64
import sys
from typing import Optional, Dict

from security_client import KMSClientHelper
from security_models import (
    DecryptionRequest,
    DecryptionResponse,
    normalize_encryption_context,
)


def decrypt_payload(
    ciphertext_b64: str,
    encryption_context: Optional[Dict[str, str]] = None,
    region: Optional[str] = None,
) -> DecryptionResponse:
    """
    Decrypt a ciphertext payload using AWS KMS managed key.

    Uses AWS KMS Decrypt API. The ciphertext blob must be the output from
    a previous AWS KMS Encrypt call with the same key and encryption context.

    Args:
        ciphertext_b64: Base64-encoded ciphertext blob from AWS KMS.
        encryption_context: Optional context that must match encryption call.
        region: AWS region override.

    Returns:
        DecryptionResponse containing plaintext and metadata.

    Raises:
        ValueError: If ciphertext_b64 is empty or invalid.
        KMSError: If AWS KMS decryption fails.
    """
    if not ciphertext_b64:
        raise ValueError("ciphertext_b64 is required")

    try:
        ciphertext_blob = base64.b64decode(ciphertext_b64)
    except Exception as e:
        raise ValueError(f"Invalid base64 ciphertext: {e}") from e

    normalized_context = normalize_encryption_context(encryption_context)

    request = DecryptionRequest(
        ciphertext_blob=ciphertext_blob,
        encryption_context=normalized_context,
    )

    kms_helper = KMSClientHelper(region=region)
    response = kms_helper.decrypt(
        ciphertext_blob=request.ciphertext_blob,
        encryption_context=request.encryption_context,
    )

    return response


def main():
    """CLI entry point for decrypt_payload."""
    ciphertext_b64 = os.environ.get("CIPHERTEXT_B64")

    if not ciphertext_b64:
        print("Error: CIPHERTEXT_B64 environment variable is required")
        sys.exit(1)

    encryption_context_str = os.environ.get("ENCRYPTION_CONTEXT")
    encryption_context = None
    if encryption_context_str:
        import json
        encryption_context = json.loads(encryption_context_str)

    try:
        response = decrypt_payload(
            ciphertext_b64=ciphertext_b64,
            encryption_context=encryption_context,
        )
        print(f"Key ID: {response.key_id}")
        print(f"Plaintext: {response.to_text()}")
    except Exception as e:
        print(f"Decryption failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
