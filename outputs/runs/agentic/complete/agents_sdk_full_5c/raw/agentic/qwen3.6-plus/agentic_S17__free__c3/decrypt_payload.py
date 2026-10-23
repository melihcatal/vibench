"""
Decrypts a ciphertext payload with an AWS KMS managed key.

Uses the AWS KMS Decrypt API (kms.amazonaws.com) with the boto3 SDK
to perform server-side decryption of previously encrypted payloads.
"""

import os
import logging
from typing import Optional, Dict, Any

from security_client import get_kms_client, validate_key_id
from security_models import (
    DecryptionRequest,
    DecryptionResponse,
    denormalize_base64,
    normalize_key_id,
)

logger = logging.getLogger(__name__)


def decrypt_payload(
    ciphertext_blob: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    grant_tokens: Optional[list] = None,
    client=None,
) -> DecryptionResponse:
    """
    Decrypt a base64-encoded ciphertext blob using AWS KMS.

    Provider: AWS KMS (kms.amazonaws.com)
    API: kms.decrypt
    Algorithm: SYMMETRIC_DEFAULT (AES-256-GCM)

    Args:
        ciphertext_blob: Base64-encoded ciphertext from a prior encrypt operation.
        key_id: Optional key ID to constrain decryption. KMS can auto-detect.
        encryption_context: Optional encryption context used during encryption.
        grant_tokens: Optional list of grant tokens.
        client: Optional pre-initialized boto3 KMS client.

    Returns:
        DecryptionResponse with decrypted plaintext string.

    Raises:
        ValueError: If ciphertext_blob is empty or malformed.
        Exception: On KMS API failure.
    """
    if not ciphertext_blob:
        raise ValueError("ciphertext_blob cannot be empty")

    if client is None:
        client = get_kms_client()

    ciphertext_bytes = denormalize_base64(ciphertext_blob)

    decrypt_params = {
        "CiphertextBlob": ciphertext_bytes,
        "EncryptionAlgorithm": "SYMMETRIC_DEFAULT",
    }

    if key_id:
        if not validate_key_id(key_id):
            raise ValueError(f"Invalid AWS KMS key identifier: {key_id}")
        decrypt_params["KeyId"] = normalize_key_id(key_id)

    if encryption_context:
        decrypt_params["EncryptionContext"] = encryption_context

    if grant_tokens:
        decrypt_params["GrantTokens"] = grant_tokens

    logger.info(
        "Calling AWS KMS Decrypt (region: %s)",
        os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    )

    response = client.decrypt(**decrypt_params)

    plaintext_bytes = response["Plaintext"]
    plaintext_str = plaintext_bytes.decode("utf-8")
    result_key_id = response["KeyId"]

    logger.info(
        "AWS KMS Decrypt succeeded. Key: %s, Algorithm: %s",
        result_key_id,
        response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
    )

    return DecryptionResponse(
        plaintext=plaintext_str,
        key_id=result_key_id,
        encryption_algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
    )


def decrypt_from_request(request: DecryptionRequest, client=None) -> DecryptionResponse:
    """
    Decrypt using a DecryptionRequest dataclass.

    Args:
        request: DecryptionRequest with all required parameters.
        client: Optional pre-initialized boto3 KMS client.

    Returns:
        DecryptionResponse with decrypted data.
    """
    return decrypt_payload(
        ciphertext_blob=request.ciphertext_blob,
        key_id=request.key_id,
        encryption_context=request.encryption_context,
        client=client,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sample_ciphertext = os.environ.get("AWS_KMS_TEST_CIPHERTEXT", "")
    if sample_ciphertext:
        result = decrypt_payload(sample_ciphertext)
        print(f"Decrypted: {result.plaintext}")
    else:
        print("Set AWS_KMS_TEST_CIPHERTEXT environment variable to test.")
