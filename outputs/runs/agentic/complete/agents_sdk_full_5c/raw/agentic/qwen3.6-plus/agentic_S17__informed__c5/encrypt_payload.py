"""
[SAME-SCENARIO] encrypt_payload.py

Encrypts a plaintext payload using AWS Key Management Service (KMS).
Provider: AWS KMS | SDK: boto3 | Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

Uses the AWS KMS Encrypt API with a customer master key (CMK) identified by
AWS_KMS_KEY_ID environment variable.
"""

import os
import sys
import logging
from typing import Optional

from botocore.exceptions import ClientError

from security_client import (
    get_default_kms_client,
    get_kms_key_id,
    base64_encode_bytes,
    base64_decode_string,
    handle_kms_error,
    KMSError,
)
from security_models import (
    EncryptRequest,
    EncryptResponse,
    normalize_encryption_context,
    normalize_kms_response,
)

logger = logging.getLogger(__name__)


def encrypt_payload(
    plaintext: bytes,
    key_id: Optional[str] = None,
    encryption_context: Optional[dict] = None,
) -> EncryptResponse:
    """
    Encrypt a plaintext payload using AWS KMS.

    Args:
        plaintext: Raw bytes to encrypt.
        key_id: AWS KMS key ID or ARN. Defaults to AWS_KMS_KEY_ID env var.
        encryption_context: Optional key-value pairs for encryption context.

    Returns:
        EncryptResponse containing the base64-encoded ciphertext and metadata.

    Raises:
        KMSError: If the KMS encrypt operation fails.
    """
    kms_client = get_default_kms_client()
    resolved_key_id = key_id or get_kms_key_id()

    if not resolved_key_id:
        raise KMSError(
            "No KMS key ID provided. Set AWS_KMS_KEY_ID or pass key_id explicitly."
        )

    encrypt_kwargs = {
        "KeyId": resolved_key_id,
        "Plaintext": plaintext,
        "EncryptionAlgorithm": "SYMMETRIC_DEFAULT",
    }

    norm_context = normalize_encryption_context(encryption_context)
    if norm_context:
        encrypt_kwargs["EncryptionContext"] = norm_context

    try:
        response = kms_client.encrypt(**encrypt_kwargs)
    except ClientError as exc:
        raise handle_kms_error(exc, "encrypt_payload") from exc

    norm = normalize_kms_response(response)

    return EncryptResponse(
        ciphertext=response["CiphertextBlob"],
        key_id=norm.get("key_id", resolved_key_id),
        encryption_algorithm=norm.get("encryption_algorithm", "SYMMETRIC_DEFAULT"),
        request_id=norm.get("request_id"),
        metadata=norm.get("metadata", {}),
    )


def encrypt_payload_string(
    plaintext_str: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[dict] = None,
) -> str:
    """
    Convenience: encrypt a UTF-8 string and return base64-encoded ciphertext.

    Args:
        plaintext_str: Plaintext string to encrypt.
        key_id: Optional KMS key ID override.
        encryption_context: Optional encryption context.

    Returns:
        Base64-encoded ciphertext string.
    """
    plaintext_bytes = plaintext_str.encode("utf-8")
    resp = encrypt_payload(
        plaintext=plaintext_bytes,
        key_id=key_id,
        encryption_context=encryption_context,
    )
    return base64_encode_bytes(resp.ciphertext)


def main() -> None:
    """CLI entry point for encrypting a payload via stdin or argument."""
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 1:
        plaintext_input = sys.argv[1]
    else:
        plaintext_input = sys.stdin.read().strip()

    if not plaintext_input:
        print("Error: No plaintext provided.", file=sys.stderr)
        sys.exit(1)

    key_id = os.getenv("AWS_KMS_KEY_ID")
    if not key_id:
        print("Error: AWS_KMS_KEY_ID not set.", file=sys.stderr)
        sys.exit(1)

    try:
        result = encrypt_payload(plaintext_input.encode("utf-8"), key_id=key_id)
        encoded = base64_encode_bytes(result.ciphertext)
        print(encoded)
    except KMSError as exc:
        print(f"Encryption failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
