"""
Uses a managed key service for signing or verification where supported.
AWS Key Management Service (boto3) is the concrete provider for asymmetric signing.

This module uses AWS KMS asymmetric keys for digital signing and verification.
"""

import os
import base64
import sys
from typing import Optional

from security_client import KMSClientHelper
from security_models import (
    SigningRequest,
    SigningResponse,
    VerificationRequest,
    VerificationResponse,
)


SIGNING_ALGORITHMS = [
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
    key_id: str,
    message: str,
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
    region: Optional[str] = None,
) -> SigningResponse:
    """
    Sign a message using AWS KMS asymmetric key.

    Uses AWS KMS Sign API with the specified asymmetric key.
    The key must be an asymmetric signing key in AWS KMS.

    Args:
        key_id: AWS KMS asymmetric key ID or ARN.
        message: The message string to sign.
        signing_algorithm: AWS KMS signing algorithm.
        region: AWS region override.

    Returns:
        SigningResponse with signature and metadata.

    Raises:
        ValueError: If key_id, message, or algorithm is invalid.
        KMSError: If AWS KMS signing fails.
    """
    if not key_id:
        raise ValueError("key_id is required")
    if not message:
        raise ValueError("message is required")
    if signing_algorithm not in SIGNING_ALGORITHMS:
        raise ValueError(f"Invalid signing algorithm: {signing_algorithm}")

    request = SigningRequest(
        key_id=key_id,
        message=message.encode("utf-8"),
        signing_algorithm=signing_algorithm,
    )

    kms_helper = KMSClientHelper(region=region)
    response = kms_helper.sign_message(
        key_id=request.key_id,
        message=request.message,
        signing_algorithm=request.signing_algorithm,
    )

    return response


def verify_signature(
    key_id: str,
    message: str,
    signature_b64: str,
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
    region: Optional[str] = None,
) -> VerificationResponse:
    """
    Verify a signature using AWS KMS asymmetric key.

    Uses AWS KMS Verify API to validate a digital signature.

    Args:
        key_id: AWS KMS asymmetric key ID or ARN.
        message: The original message string.
        signature_b64: Base64-encoded signature to verify.
        signing_algorithm: AWS KMS signing algorithm used for signing.
        region: AWS region override.

    Returns:
        VerificationResponse with is_valid flag.

    Raises:
        ValueError: If inputs are invalid.
        KMSError: If AWS KMS verification fails.
    """
    if not key_id:
        raise ValueError("key_id is required")
    if not message:
        raise ValueError("message is required")
    if not signature_b64:
        raise ValueError("signature_b64 is required")

    try:
        signature = base64.b64decode(signature_b64)
    except Exception as e:
        raise ValueError(f"Invalid base64 signature: {e}") from e

    request = VerificationRequest(
        key_id=key_id,
        message=message.encode("utf-8"),
        signature=signature,
        signing_algorithm=signing_algorithm,
    )

    kms_helper = KMSClientHelper(region=region)
    response = kms_helper.verify_signature(
        key_id=request.key_id,
        message=request.message,
        signature=request.signature,
        signing_algorithm=request.signing_algorithm,
    )

    return response


def main():
    """CLI entry point for sign_or_verify_key."""
    action = os.environ.get("ACTION", "sign")
    key_id = os.environ.get("KMS_KEY_ID")

    if not key_id:
        print("Error: KMS_KEY_ID environment variable is required")
        sys.exit(1)

    algorithm = os.environ.get("SIGNING_ALGORITHM", "RSASSA_PKCS1_V1_5_SHA_256")

    if action == "sign":
        message = os.environ.get("MESSAGE", "message-to-sign")

        try:
            response = sign_message(
                key_id=key_id,
                message=message,
                signing_algorithm=algorithm,
            )
            print(f"Key ID: {response.key_id}")
            print(f"Algorithm: {response.signing_algorithm}")
            print(f"Signature (base64): {response.to_base64()}")
        except Exception as e:
            print(f"Signing failed: {e}")
            sys.exit(1)

    elif action == "verify":
        message = os.environ.get("MESSAGE")
        signature_b64 = os.environ.get("SIGNATURE_B64")

        if not message or not signature_b64:
            print("Error: MESSAGE and SIGNATURE_B64 are required for verification")
            sys.exit(1)

        try:
            response = verify_signature(
                key_id=key_id,
                message=message,
                signature_b64=signature_b64,
                signing_algorithm=algorithm,
            )
            print(f"Key ID: {response.key_id}")
            print(f"Signature Valid: {response.is_valid}")
        except Exception as e:
            print(f"Verification failed: {e}")
            sys.exit(1)

    else:
        print(f"Unknown action: {action}. Use 'sign' or 'verify'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
