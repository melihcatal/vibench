"""
Encrypts a plaintext payload with an AWS managed key using AWS KMS.
Uses the AWS KMS Encrypt API with boto3 to encrypt data under a customer master key.
"""

import json
import sys
import logging

from security_client import create_kms_client, get_default_key_id, handle_kms_error, build_encryption_context
from security_models import (
    EncryptionRequest,
    EncryptionResponse,
    parse_aws_kms_encrypt_response,
    normalize_encryption_context,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def encrypt_payload(
    plaintext: str,
    key_id: str = "",
    encryption_context: dict = None,
    algorithm: str = "SYMMETRIC_DEFAULT",
) -> EncryptionResponse:
    """
    Encrypt a plaintext payload using AWS KMS Encrypt API.

    Provider: AWS KMS (boto3) - kms.us-east-1.amazonaws.com
    Model/Algorithm: SYMMETRIC_DEFAULT (AES-256-GCM)

    Args:
        plaintext: The plaintext string to encrypt.
        key_id: The AWS KMS key ID or ARN.
        encryption_context: Optional encryption context for additional authenticated data.
        algorithm: Encryption algorithm (default: SYMMETRIC_DEFAULT).

    Returns:
        EncryptionResponse with base64-encoded ciphertext and metadata.
    """
    request = EncryptionRequest(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=encryption_context or {},
        algorithm=algorithm,
    )

    kms_client = create_kms_client()
    if not request.key_id:
        request.key_id = get_default_key_id()

    normalized_context = normalize_encryption_context(request.encryption_context)
    plaintext_bytes = request.to_normalized_payload()

    try:
        kms_params = {
            "KeyId": request.key_id,
            "Plaintext": plaintext_bytes,
            "EncryptionAlgorithm": request.algorithm,
        }
        if normalized_context:
            kms_params["EncryptionContext"] = normalized_context

        logger.info("Encrypting payload with AWS KMS key %s", request.key_id)
        response = kms_client.encrypt(**kms_params)

        result = parse_aws_kms_encrypt_response(response)
        logger.info("Encryption successful, request_id=%s", result.request_id)
        return result

    except Exception as e:
        if hasattr(e, "response"):
            error_info = handle_kms_error(e, "encrypt")
            raise RuntimeError(f"KMS encryption failed: {error_info}") from e
        raise


def encrypt_from_args(plaintext: str, key_id: str = "", context_json: str = None) -> str:
    """
    Convenience function for CLI or external invocation.

    Args:
        plaintext: Text to encrypt.
        key_id: KMS key identifier.
        context_json: JSON string of encryption context.

    Returns:
        JSON string of EncryptionResponse.
    """
    encryption_context = json.loads(context_json) if context_json else {}
    result = encrypt_payload(plaintext, key_id, encryption_context)
    return result.to_json()


if __name__ == "__main__":
    sample_plaintext = "This is a secret payload to encrypt with AWS KMS."
    result = encrypt_payload(sample_plaintext)
    print(result.to_json())
