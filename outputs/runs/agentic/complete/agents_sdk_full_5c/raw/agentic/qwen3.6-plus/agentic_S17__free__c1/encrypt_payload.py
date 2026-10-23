"""
encrypt_payload.py - Encrypts a plaintext payload with a managed key using AWS KMS.

Uses the AWS Key Management Service (KMS) Encrypt API to encrypt plaintext data
with a customer master key (CMK). Supports optional encryption context for
additional authenticated data (AAD).

Provider: AWS KMS (boto3 client for kms.us-east-1.amazonaws.com)
Model/Key Type: SYMMETRIC_DEFAULT (AES-256-GCM) or RSAES_OAEP_SHA_256
"""

import json
import logging
import sys
from typing import Optional

from security_client import get_kms_client, load_encryption_context, validate_key_id
from security_models import (
    EncryptionRequest,
    EncryptionResponse,
    encode_ciphertext,
    normalize_encryption_response,
)

logger = logging.getLogger(__name__)


def encrypt_payload(
    plaintext: str,
    key_id: str,
    encryption_context: Optional[str] = None,
    algorithm: str = "SYMMETRIC_DEFAULT",
    region: Optional[str] = None,
) -> EncryptionResponse:
    """
    Encrypt a plaintext payload using AWS KMS.

    Args:
        plaintext: The plaintext string to encrypt.
        key_id: The KMS key ID, ARN, or alias (e.g., alias/my-key).
        encryption_context: Optional JSON string of key-value pairs for AAD.
        algorithm: Encryption algorithm. SYMMETRIC_DEFAULT or RSAES_OAEP_SHA_256.
        region: AWS region override.

    Returns:
        EncryptionResponse with base64-encoded ciphertext and metadata.

    Raises:
        ValueError: If key_id is invalid.
        RuntimeError: If KMS encryption fails.
    """
    validate_key_id(key_id)

    kms_client = get_kms_client(region_name=region)

    encryption_ctx = load_encryption_context(encryption_context)

    encrypt_kwargs = {
        "KeyId": key_id,
        "Plaintext": plaintext.encode("utf-8"),
    }

    if encryption_ctx:
        encrypt_kwargs["EncryptionContext"] = encryption_ctx

    if algorithm != "SYMMETRIC_DEFAULT":
        encrypt_kwargs["EncryptionAlgorithm"] = algorithm

    request = EncryptionRequest(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=encryption_ctx if encryption_ctx else None,
        algorithm=algorithm,
    )

    try:
        raw_response = kms_client.encrypt(**encrypt_kwargs)
    except Exception as e:
        raise RuntimeError(f"AWS KMS Encrypt failed: {e}") from e

    response = normalize_encryption_response(raw_response)
    logger.info(
        "Encrypted payload with KMS key %s, algorithm %s",
        response.key_id,
        response.encryption_algorithm,
    )
    return response


def main():
    """CLI entry point for encrypt_payload."""
    if len(sys.argv) < 3:
        print("Usage: python encrypt_payload.py <key_id> <plaintext> [encryption_context_json]")
        sys.exit(1)

    key_id = sys.argv[1]
    plaintext = sys.argv[2]
    context = sys.argv[3] if len(sys.argv) > 3 else None

    logging.basicConfig(level=logging.INFO)
    result = encrypt_payload(plaintext, key_id, encryption_context=context)

    output = {
        "ciphertext_blob": result.ciphertext_blob,
        "key_id": result.key_id,
        "encryption_algorithm": result.encryption_algorithm,
        "metadata": result.metadata,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
