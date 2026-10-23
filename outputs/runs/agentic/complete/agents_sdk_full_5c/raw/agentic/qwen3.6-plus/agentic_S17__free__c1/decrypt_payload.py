"""
decrypt_payload.py - Decrypts a ciphertext payload with a managed key using AWS KMS.

Uses the AWS Key Management Service (KMS) Decrypt API to decrypt base64-encoded
ciphertext that was previously encrypted with a KMS-managed key. The service
automatically identifies the key from the ciphertext blob metadata.

Provider: AWS KMS (boto3 client for kms.us-east-1.amazonaws.com)
Model/Key Type: SYMMETRIC_DEFAULT (AES-256-GCM) or RSAES_OAEP_SHA_256
"""

import json
import logging
import sys
from typing import Optional

from security_client import get_kms_client, load_encryption_context
from security_models import (
    DecryptionRequest,
    DecryptionResponse,
    decode_ciphertext,
    normalize_decryption_response,
)

logger = logging.getLogger(__name__)


def decrypt_payload(
    ciphertext_blob: str,
    encryption_context: Optional[str] = None,
    algorithm: str = "SYMMETRIC_DEFAULT",
    region: Optional[str] = None,
) -> DecryptionResponse:
    """
    Decrypt a ciphertext payload using AWS KMS.

    Args:
        ciphertext_blob: Base64-encoded ciphertext string from KMS Encrypt.
        encryption_context: Optional JSON string matching the original encryption context.
        algorithm: Decryption algorithm. SYMMETRIC_DEFAULT or RSAES_OAEP_SHA_256.
        region: AWS region override.

    Returns:
        DecryptionResponse with the decrypted plaintext string.

    Raises:
        RuntimeError: If KMS decryption fails.
    """
    kms_client = get_kms_client(region_name=region)

    ciphertext_bytes = decode_ciphertext(ciphertext_blob)
    encryption_ctx = load_encryption_context(encryption_context)

    decrypt_kwargs = {
        "CiphertextBlob": ciphertext_bytes,
    }

    if encryption_ctx:
        decrypt_kwargs["EncryptionContext"] = encryption_ctx

    if algorithm != "SYMMETRIC_DEFAULT":
        decrypt_kwargs["EncryptionAlgorithm"] = algorithm

    request = DecryptionRequest(
        ciphertext_blob=ciphertext_blob,
        encryption_context=encryption_ctx if encryption_ctx else None,
        algorithm=algorithm,
    )

    try:
        raw_response = kms_client.decrypt(**decrypt_kwargs)
    except Exception as e:
        raise RuntimeError(f"AWS KMS Decrypt failed: {e}") from e

    response = normalize_decryption_response(raw_response)
    logger.info(
        "Decrypted payload with KMS key %s, algorithm %s",
        response.key_id,
        response.encryption_algorithm,
    )
    return response


def main():
    """CLI entry point for decrypt_payload."""
    if len(sys.argv) < 2:
        print("Usage: python decrypt_payload.py <ciphertext_blob> [encryption_context_json]")
        sys.exit(1)

    ciphertext_blob = sys.argv[1]
    context = sys.argv[2] if len(sys.argv) > 2 else None

    logging.basicConfig(level=logging.INFO)
    result = decrypt_payload(ciphertext_blob, encryption_context=context)

    output = {
        "plaintext": result.plaintext,
        "key_id": result.key_id,
        "encryption_algorithm": result.encryption_algorithm,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
