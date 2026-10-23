"""
Decrypts a ciphertext payload with an AWS managed key using AWS KMS.
Uses the AWS KMS Decrypt API with boto3 to decrypt data encrypted under a customer master key.
"""

import json
import sys
import logging

from security_client import create_kms_client, handle_kms_error, build_encryption_context
from security_models import (
    DecryptionRequest,
    DecryptionResponse,
    parse_aws_kms_decrypt_response,
    normalize_encryption_context,
    decode_ciphertext,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def decrypt_payload(
    ciphertext: str,
    key_id: str = "",
    encryption_context: dict = None,
    algorithm: str = None,
) -> DecryptionResponse:
    """
    Decrypt a ciphertext payload using AWS KMS Decrypt API.

    Provider: AWS KMS (boto3) - kms.us-east-1.amazonaws.com
    Algorithm: SYMMETRIC_DEFAULT (AES-256-GCM) or specified algorithm.

    Args:
        ciphertext: Base64-encoded ciphertext blob from KMS Encrypt.
        key_id: Optional KMS key ID (KMS can derive from ciphertext).
        encryption_context: Encryption context used during encryption.
        algorithm: Optional decryption algorithm override.

    Returns:
        DecryptionResponse with decrypted plaintext.
    """
    request = DecryptionRequest(
        ciphertext=ciphertext,
        encryption_context=encryption_context or {},
        algorithm=algorithm,
    )

    kms_client = create_kms_client()
    normalized_context = normalize_encryption_context(request.encryption_context)
    ciphertext_bytes = request.get_ciphertext_bytes()

    try:
        kms_params = {
            "CiphertextBlob": ciphertext_bytes,
        }
        if key_id:
            kms_params["KeyId"] = key_id
        if normalized_context:
            kms_params["EncryptionContext"] = normalized_context
        if request.algorithm:
            kms_params["EncryptionAlgorithm"] = request.algorithm

        logger.info("Decrypting payload with AWS KMS")
        response = kms_client.decrypt(**kms_params)

        result = parse_aws_kms_decrypt_response(response)
        logger.info("Decryption successful, request_id=%s, key_id=%s", result.request_id, result.key_id)
        return result

    except Exception as e:
        if hasattr(e, "response"):
            error_info = handle_kms_error(e, "decrypt")
            raise RuntimeError(f"KMS decryption failed: {error_info}") from e
        raise


def decrypt_from_args(ciphertext: str, key_id: str = "", context_json: str = None) -> str:
    """
    Convenience function for CLI or external invocation.

    Args:
        ciphertext: Base64 ciphertext to decrypt.
        key_id: Optional KMS key identifier.
        context_json: JSON string of encryption context.

    Returns:
        JSON string of DecryptionResponse.
    """
    encryption_context = json.loads(context_json) if context_json else {}
    result = decrypt_payload(ciphertext, key_id, encryption_context)
    return result.to_json()


if __name__ == "__main__":
    import base64
    sample_ciphertext = base64.b64encode(b"sample_ciphertext_blob").decode("utf-8")
    result = decrypt_payload(sample_ciphertext)
    print(result.to_json())
