"""
Uses AWS KMS managed keys for signing or verification.

Uses the AWS KMS Sign and Verify APIs (kms.amazonaws.com) with the boto3 SDK
to perform asymmetric cryptographic signing and verification operations
using RSA or ECDSA keys managed by AWS KMS.
"""

import os
import logging
from typing import Optional, Dict, Any

from security_client import get_kms_client, validate_key_id
from security_models import (
    SigningRequest,
    SigningResponse,
    VerificationRequest,
    VerificationResponse,
    normalize_base64,
    denormalize_base64,
    normalize_key_id,
)

logger = logging.getLogger(__name__)

SUPPORTED_SIGNING_ALGORITHMS = [
    "RSASSA_PKCS1_V1_5_SHA_256",
    "RSASSA_PKCS1_V1_5_SHA_384",
    "RSASSA_PKCS1_V1_5_SHA_512",
    "RSASSA_PSS_SHA_256",
    "RSASSA_PSS_SHA_384",
    "RSASSA_PSS_SHA_512",
    "ECDSA_SHA_256",
    "ECDSA_SHA_384",
    "ECDSA_SHA_512",
]


def sign_message(
    message: str,
    key_id: str,
    signing_algorithm: str = "RSASSA_PSS_SHA_256",
    message_type: str = "RAW",
    grant_tokens: Optional[list] = None,
    client=None,
) -> SigningResponse:
    """
    Sign a message using an AWS KMS asymmetric signing key.

    Provider: AWS KMS (kms.amazonaws.com)
    API: kms.sign
    Supported algorithms: RSASSA_PSS_SHA_256, ECDSA_SHA_256, etc.

    Args:
        message: The message string to sign.
        key_id: AWS KMS asymmetric signing key ID or ARN.
        signing_algorithm: Signing algorithm (default: RSASSA_PSS_SHA_256).
        message_type: 'RAW' or 'DIGEST' (default: 'RAW').
        grant_tokens: Optional grant tokens.
        client: Optional pre-initialized boto3 KMS client.

    Returns:
        SigningResponse with base64-encoded signature.

    Raises:
        ValueError: If key_id is invalid or algorithm unsupported.
        Exception: On KMS API failure.
    """
    if not validate_key_id(key_id):
        raise ValueError(f"Invalid AWS KMS key identifier: {key_id}")

    if signing_algorithm not in SUPPORTED_SIGNING_ALGORITHMS:
        raise ValueError(
            f"Unsupported signing algorithm: {signing_algorithm}. "
            f"Must be one of: {SUPPORTED_SIGNING_ALGORITHMS}"
        )

    if client is None:
        client = get_kms_client()

    normalized_key = normalize_key_id(key_id)
    message_bytes = message.encode("utf-8")

    sign_params = {
        "KeyId": normalized_key,
        "Message": message_bytes,
        "SigningAlgorithm": signing_algorithm,
        "MessageType": message_type,
    }

    if grant_tokens:
        sign_params["GrantTokens"] = grant_tokens

    logger.info(
        "Calling AWS KMS Sign for key %s, algorithm %s (region: %s)",
        normalized_key,
        signing_algorithm,
        os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    )

    response = client.sign(**sign_params)

    signature_bytes = response["Signature"]

    result = SigningResponse(
        signature=normalize_base64(signature_bytes),
        key_id=response.get("KeyId", normalized_key),
        signing_algorithm=response.get("SigningAlgorithm", signing_algorithm),
    )

    logger.info(
        "AWS KMS Sign succeeded. Key: %s, Algorithm: %s",
        result.key_id,
        result.signing_algorithm,
    )

    return result


def verify_signature(
    message: str,
    signature: str,
    key_id: str,
    signing_algorithm: str = "RSASSA_PSS_SHA_256",
    message_type: str = "RAW",
    grant_tokens: Optional[list] = None,
    client=None,
) -> VerificationResponse:
    """
    Verify a signature using an AWS KMS asymmetric signing key.

    Provider: AWS KMS (kms.amazonaws.com)
    API: kms.verify
    Supported algorithms: RSASSA_PSS_SHA_256, ECDSA_SHA_256, etc.

    Args:
        message: The original message string.
        signature: Base64-encoded signature to verify.
        key_id: AWS KMS asymmetric signing key ID or ARN.
        signing_algorithm: Signing algorithm used (default: RSASSA_PSS_SHA_256).
        message_type: 'RAW' or 'DIGEST' (default: 'RAW').
        grant_tokens: Optional grant tokens.
        client: Optional pre-initialized boto3 KMS client.

    Returns:
        VerificationResponse with validation result.

    Raises:
        ValueError: If key_id is invalid.
        Exception: On KMS API failure.
    """
    if not validate_key_id(key_id):
        raise ValueError(f"Invalid AWS KMS key identifier: {key_id}")

    if client is None:
        client = get_kms_client()

    normalized_key = normalize_key_id(key_id)
    message_bytes = message.encode("utf-8")
    signature_bytes = denormalize_base64(signature)

    verify_params = {
        "KeyId": normalized_key,
        "Message": message_bytes,
        "Signature": signature_bytes,
        "SigningAlgorithm": signing_algorithm,
        "MessageType": message_type,
    }

    if grant_tokens:
        verify_params["GrantTokens"] = grant_tokens

    logger.info(
        "Calling AWS KMS Verify for key %s, algorithm %s (region: %s)",
        normalized_key,
        signing_algorithm,
        os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    )

    try:
        response = client.verify(**verify_params)
        is_valid = response.get("SignatureValid", False)

        logger.info(
            "AWS KMS Verify result: %s (key: %s)",
            "VALID" if is_valid else "INVALID",
            response.get("KeyId", normalized_key),
        )

        return VerificationResponse(
            is_valid=is_valid,
            key_id=response.get("KeyId", normalized_key),
            signing_algorithm=signing_algorithm,
        )
    except client.exceptions.KMSInvalidSignatureException:
        return VerificationResponse(
            is_valid=False,
            key_id=normalized_key,
            signing_algorithm=signing_algorithm,
        )


def sign_from_request(request: SigningRequest, client=None) -> SigningResponse:
    """
    Sign using a SigningRequest dataclass.

    Args:
        request: SigningRequest with all required parameters.
        client: Optional pre-initialized boto3 KMS client.

    Returns:
        SigningResponse with signature.
    """
    return sign_message(
        message=request.message,
        key_id=request.key_id,
        signing_algorithm=request.signing_algorithm,
        message_type=request.message_type,
        client=client,
    )


def verify_from_request(
    request: VerificationRequest, client=None
) -> VerificationResponse:
    """
    Verify using a VerificationRequest dataclass.

    Args:
        request: VerificationRequest with all required parameters.
        client: Optional pre-initialized boto3 KMS client.

    Returns:
        VerificationResponse with validation result.
    """
    return verify_signature(
        message=request.message,
        signature=request.signature,
        key_id=request.key_id,
        signing_algorithm=request.signing_algorithm,
        client=client,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sample_signing_key = os.environ.get("AWS_KMS_SIGNING_KEY_ID", "")
    if sample_signing_key:
        sign_result = sign_message(
            "Message to sign with AWS KMS",
            sample_signing_key,
            signing_algorithm="RSASSA_PSS_SHA_256",
        )
        print(f"Signed with key: {sign_result.key_id}")
        print(f"Signature: {sign_result.signature[:60]}...")

        verify_result = verify_signature(
            "Message to sign with AWS KMS",
            sign_result.signature,
            sample_signing_key,
            signing_algorithm="RSASSA_PSS_SHA_256",
        )
        print(f"Signature valid: {verify_result.is_valid}")
    else:
        print("Set AWS_KMS_SIGNING_KEY_ID environment variable to test.")
