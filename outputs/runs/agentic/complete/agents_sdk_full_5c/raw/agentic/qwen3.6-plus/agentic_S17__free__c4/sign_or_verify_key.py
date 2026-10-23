"""
Uses AWS KMS managed key service for signing or signature verification.
Supports RSA and ECDSA signing algorithms via AWS KMS Sign and Verify APIs.
"""

import json
import hashlib
import logging

from security_client import create_kms_client, get_default_key_id, handle_kms_error
from security_models import (
    SigningRequest,
    SigningResponse,
    VerificationRequest,
    VerificationResponse,
    parse_aws_kms_sign_response,
    parse_aws_kms_verify_response,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# AWS KMS signing algorithm identifiers
AWS_KMS_SIGN_ALGORITHM_RSA_PSS_SHA256 = "RSASSA_PSS_SHA_256"
AWS_KMS_SIGN_ALGORITHM_RSA_PSS_SHA384 = "RSASSA_PSS_SHA_384"
AWS_KMS_SIGN_ALGORITHM_RSA_PSS_SHA512 = "RSASSA_PSS_SHA_512"
AWS_KMS_SIGN_ALGORITHM_RSA_PKCS1_SHA256 = "RSASSA_PKCS1_V1_5_SHA_256"
AWS_KMS_SIGN_ALGORITHM_ECDSA_SHA256 = "ECDSA_SHA_256"
AWS_KMS_SIGN_ALGORITHM_ECDSA_SHA384 = "ECDSA_SHA_384"
AWS_KMS_SIGN_ALGORITHM_ECDSA_SHA512 = "ECDSA_SHA_512"

SUPPORTED_SIGNING_ALGORITHMS = [
    AWS_KMS_SIGN_ALGORITHM_RSA_PSS_SHA256,
    AWS_KMS_SIGN_ALGORITHM_RSA_PSS_SHA384,
    AWS_KMS_SIGN_ALGORITHM_RSA_PSS_SHA512,
    AWS_KMS_SIGN_ALGORITHM_RSA_PKCS1_SHA256,
    AWS_KMS_SIGN_ALGORITHM_ECDSA_SHA256,
    AWS_KMS_SIGN_ALGORITHM_ECDSA_SHA384,
    AWS_KMS_SIGN_ALGORITHM_ECDSA_SHA512,
]


def sign_message(
    message: str,
    key_id: str = "",
    algorithm: str = AWS_KMS_SIGN_ALGORITHM_RSA_PSS_SHA256,
    message_type: str = "RAW",
) -> SigningResponse:
    """
    Sign a message using AWS KMS Sign API.

    Provider: AWS KMS (boto3) - kms.us-east-1.amazonaws.com
    Supported algorithms: RSASSA_PSS_SHA_256, ECDSA_SHA_256, etc.

    Args:
        message: The message string to sign.
        key_id: AWS KMS asymmetric signing key ID or ARN.
        algorithm: Signing algorithm (default: RSASSA_PSS_SHA_256).
        message_type: Message type - RAW or DIGEST (default: RAW).

    Returns:
        SigningResponse with base64-encoded signature and metadata.
    """
    request = SigningRequest(
        message=message,
        key_id=key_id,
        message_type=message_type,
        algorithm=algorithm,
    )

    if algorithm not in SUPPORTED_SIGNING_ALGORITHMS:
        raise ValueError(
            f"Unsupported signing algorithm: {algorithm}. "
            f"Supported: {SUPPORTED_SIGNING_ALGORITHMS}"
        )

    kms_client = create_kms_client()
    if not request.key_id:
        request.key_id = get_default_key_id()

    message_bytes = request.get_message_bytes()

    try:
        kms_params = {
            "KeyId": request.key_id,
            "Message": message_bytes,
            "MessageType": request.message_type,
            "SigningAlgorithm": request.algorithm,
        }

        logger.info("Signing message with AWS KMS key %s, algorithm %s",
                     request.key_id, request.algorithm)
        response = kms_client.sign(**kms_params)

        result = parse_aws_kms_sign_response(response)
        logger.info("Signing successful, request_id=%s", result.request_id)
        return result

    except Exception as e:
        if hasattr(e, "response"):
            error_info = handle_kms_error(e, "sign")
            raise RuntimeError(f"KMS signing failed: {error_info}") from e
        raise


def verify_signature(
    message: str,
    signature: str,
    key_id: str = "",
    algorithm: str = AWS_KMS_SIGN_ALGORITHM_RSA_PSS_SHA256,
    message_type: str = "RAW",
) -> VerificationResponse:
    """
    Verify a signature using AWS KMS Verify API.

    Provider: AWS KMS (boto3) - kms.us-east-1.amazonaws.com
    Supported algorithms: RSASSA_PSS_SHA_256, ECDSA_SHA_256, etc.

    Args:
        message: The original message string.
        signature: Base64-encoded signature to verify.
        key_id: AWS KMS signing key ID or ARN.
        algorithm: Signing algorithm used to create the signature.
        message_type: Message type - RAW or DIGEST.

    Returns:
        VerificationResponse with is_valid flag.
    """
    request = VerificationRequest(
        message=message,
        signature=signature,
        key_id=key_id,
        message_type=message_type,
        algorithm=algorithm,
    )

    if algorithm not in SUPPORTED_SIGNING_ALGORITHMS:
        raise ValueError(
            f"Unsupported signing algorithm: {algorithm}. "
            f"Supported: {SUPPORTED_SIGNING_ALGORITHMS}"
        )

    kms_client = create_kms_client()
    if not request.key_id:
        request.key_id = get_default_key_id()

    message_bytes = request.get_message_bytes()
    signature_bytes = request.get_signature_bytes()

    try:
        kms_params = {
            "KeyId": request.key_id,
            "Message": message_bytes,
            "MessageType": request.message_type,
            "Signature": signature_bytes,
            "SigningAlgorithm": request.algorithm,
        }

        logger.info("Verifying signature with AWS KMS key %s", request.key_id)
        response = kms_client.verify(**kms_params)

        result = parse_aws_kms_verify_response(response)
        logger.info("Verification result: valid=%s, request_id=%s",
                     result.is_valid, result.request_id)
        return result

    except Exception as e:
        if hasattr(e, "response"):
            error_info = handle_kms_error(e, "verify")
            raise RuntimeError(f"KMS verification failed: {error_info}") from e
        raise


def sign_or_verify(
    action: str,
    message: str,
    key_id: str = "",
    signature: str = "",
    algorithm: str = AWS_KMS_SIGN_ALGORITHM_RSA_PSS_SHA256,
) -> dict:
    """
    Unified sign or verify operation.

    Args:
        action: "sign" or "verify".
        message: Message to sign or verify.
        key_id: KMS asymmetric signing key ID.
        signature: Base64 signature (required for verify).
        algorithm: Signing algorithm.

    Returns:
        Dict with operation result.
    """
    if action.lower() == "sign":
        result = sign_message(message, key_id, algorithm)
        return {"action": "sign", **result.to_dict()}
    elif action.lower() == "verify":
        if not signature:
            raise ValueError("Signature is required for verification")
        result = verify_signature(message, signature, key_id, algorithm)
        return {"action": "verify", **result.to_dict()}
    else:
        raise ValueError(f"Unsupported action: {action}. Use 'sign' or 'verify'.")


if __name__ == "__main__":
    sample_message = "Document to sign with AWS KMS asymmetric key."
    sign_result = sign_message(sample_message)
    print("Sign result:", sign_result.to_json())
