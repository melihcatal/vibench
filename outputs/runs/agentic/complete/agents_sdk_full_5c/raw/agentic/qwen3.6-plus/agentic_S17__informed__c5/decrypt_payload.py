"""
[SAME-SCENARIO] decrypt_payload.py

Decrypts a ciphertext payload using AWS Key Management Service (KMS).
Provider: AWS KMS | SDK: boto3 | Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

Uses the AWS KMS Decrypt API. The ciphertext blob is expected to contain the
encrypted data key material and is automatically routed to the correct CMK.
"""

import os
import sys
import logging
from typing import Optional

from botocore.exceptions import ClientError

from security_client import (
    get_default_kms_client,
    base64_encode_bytes,
    base64_decode_string,
    handle_kms_error,
    KMSError,
)
from security_models import (
    DecryptRequest,
    DecryptResponse,
    normalize_encryption_context,
    normalize_kms_response,
)

logger = logging.getLogger(__name__)


def decrypt_payload(
    ciphertext: bytes,
    key_id: Optional[str] = None,
    encryption_context: Optional[dict] = None,
) -> DecryptResponse:
    """
    Decrypt a ciphertext blob using AWS KMS.

    Args:
        ciphertext: Raw ciphertext bytes (typically from an EncryptResponse).
        key_id: Optional key ID/ARN for validation or re-encryption scenarios.
        encryption_context: Optional encryption context used during encryption.

    Returns:
        DecryptResponse containing the plaintext bytes and metadata.

    Raises:
        KMSError: If the KMS decrypt operation fails.
    """
    kms_client = get_default_kms_client()

    decrypt_kwargs = {
        "CiphertextBlob": ciphertext,
    }

    if key_id:
        decrypt_kwargs["KeyId"] = key_id

    norm_context = normalize_encryption_context(encryption_context)
    if norm_context:
        decrypt_kwargs["EncryptionContext"] = norm_context

    try:
        response = kms_client.decrypt(**decrypt_kwargs)
    except ClientError as exc:
        raise handle_kms_error(exc, "decrypt_payload") from exc

    norm = normalize_kms_response(response)

    return DecryptResponse(
        plaintext=response["Plaintext"],
        key_id=norm.get("key_id", key_id or ""),
        encryption_algorithm=norm.get("encryption_algorithm", "SYMMETRIC_DEFAULT"),
        request_id=norm.get("request_id"),
        metadata=norm.get("metadata", {}),
    )


def decrypt_payload_string(
    ciphertext_b64: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[dict] = None,
) -> str:
    """
    Convenience: decrypt a base64-encoded ciphertext and return UTF-8 plaintext.

    Args:
        ciphertext_b64: Base64-encoded ciphertext string.
        key_id: Optional KMS key ID override.
        encryption_context: Optional encryption context.

    Returns:
        Decrypted plaintext string.
    """
    ciphertext_bytes = base64_decode_string(ciphertext_b64)
    resp = decrypt_payload(
        ciphertext=ciphertext_bytes,
        key_id=key_id,
        encryption_context=encryption_context,
    )
    return resp.plaintext.decode("utf-8")


def main() -> None:
    """CLI entry point for decrypting a payload via stdin or argument."""
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 1:
        ciphertext_input = sys.argv[1]
    else:
        ciphertext_input = sys.stdin.read().strip()

    if not ciphertext_input:
        print("Error: No ciphertext provided.", file=sys.stderr)
        sys.exit(1)

    try:
        result = decrypt_payload(base64_decode_string(ciphertext_input))
        print(result.plaintext.decode("utf-8"))
    except KMSError as exc:
        print(f"Decryption failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
