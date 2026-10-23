"""
sign_or_verify_key.py - Uses AWS KMS managed key service for signing or verification.

Provider: AWS Key Management Service (KMS)
Service endpoint: kms.{region}.amazonaws.com
Concrete model: AWS KMS asymmetric signing (RSASSA_PKCS1_V1_5_SHA_256 / ECDSA_SHA_256)
"""

from __future__ import annotations

import os
from typing import Optional

from security_client import (
    SecurityClientConfig,
    create_kms_client,
    handle_kms_error,
    extract_key_arn_from_response,
)
from security_models import (
    SignRequest,
    SignResponse,
    VerifyRequest,
    VerifyResponse,
    encode_bytes,
    decode_bytes,
    normalize_key_id,
)

SUPPORTED_SIGNING_ALGORITHMS = {
    "RSASSA_PKCS1_V1_5_SHA_256",
    "RSASSA_PKCS1_V1_5_SHA_384",
    "RSASSA_PKCS1_V1_5_SHA_512",
    "RSASSA_PSS_SHA_256",
    "RSASSA_PSS_SHA_384",
    "RSASSA_PSS_SHA_512",
    "ECDSA_SHA_256",
    "ECDSA_SHA_384",
    "ECDSA_SHA_512",
}


def sign_message(
    message: str,
    key_id: str,
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
    message_type: str = "RAW",
    config: Optional[SecurityClientConfig] = None,
) -> SignResponse:
    """
    Sign a message using an AWS KMS asymmetric key.

    Uses the AWS KMS Sign API. The key must be an asymmetric KMS key
    configured for signing operations. Supported algorithms include
    RSASSA_PKCS1_V1_5_SHA_256, RSASSA_PSS_SHA_256, and ECDSA_SHA_256.

    Args:
        message: The message to sign.
        key_id: AWS KMS asymmetric key ID or ARN.
        signing_algorithm: KMS signing algorithm identifier.
        message_type: "RAW" for raw bytes, "DIGEST" for pre-computed digest.
        config: Optional SecurityClientConfig.

    Returns:
        SignResponse with base64-encoded signature.
    """
    if signing_algorithm not in SUPPORTED_SIGNING_ALGORITHMS:
        raise ValueError(
            f"Unsupported signing algorithm: {signing_algorithm}. "
            f"Must be one of {SUPPORTED_SIGNING_ALGORITHMS}"
        )

    kms_client = create_kms_client(config)
    normalized_key_id = normalize_key_id(key_id)

    message_bytes = message.encode("utf-8")

    sign_kwargs = {
        "KeyId": normalized_key_id,
        "Message": message_bytes,
        "SigningAlgorithm": signing_algorithm,
        "MessageType": message_type,
    }

    try:
        response = kms_client.sign(**sign_kwargs)
    except Exception as e:
        handle_kms_error(e, context="sign_or_verify_key:sign_message")

    signature = encode_bytes(response["Signature"])
    response_key_id = extract_key_arn_from_response(response, normalized_key_id)

    return SignResponse(
        signature=signature,
        key_id=response_key_id,
        signing_algorithm=signing_algorithm,
    )


def verify_signature(
    message: str,
    signature: str,
    key_id: str,
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
    message_type: str = "RAW",
    config: Optional[SecurityClientConfig] = None,
) -> VerifyResponse:
    """
    Verify a signature using an AWS KMS asymmetric key.

    Uses the AWS KMS Verify API. The signature must have been generated
    by the same KMS key with the same algorithm.

    Args:
        message: The original message that was signed.
        signature: Base64-encoded signature to verify.
        key_id: AWS KMS asymmetric key ID or ARN used for signing.
        signing_algorithm: Algorithm used during signing.
        message_type: "RAW" or "DIGEST".
        config: Optional SecurityClientConfig.

    Returns:
        VerifyResponse with verification result.
    """
    if signing_algorithm not in SUPPORTED_SIGNING_ALGORITHMS:
        raise ValueError(
            f"Unsupported signing algorithm: {signing_algorithm}. "
            f"Must be one of {SUPPORTED_SIGNING_ALGORITHMS}"
        )

    kms_client = create_kms_client(config)
    normalized_key_id = normalize_key_id(key_id)

    message_bytes = message.encode("utf-8")
    signature_bytes = decode_bytes(signature)

    verify_kwargs = {
        "KeyId": normalized_key_id,
        "Message": message_bytes,
        "Signature": signature_bytes,
        "SigningAlgorithm": signing_algorithm,
        "MessageType": message_type,
    }

    try:
        response = kms_client.verify(**verify_kwargs)
    except Exception as e:
        handle_kms_error(e, context="sign_or_verify_key:verify_signature")

    is_valid = response.get("SignatureValid", False)
    response_key_id = extract_key_arn_from_response(response, normalized_key_id)

    return VerifyResponse(
        is_valid=is_valid,
        key_id=response_key_id,
        signing_algorithm=signing_algorithm,
    )


def sign_from_request(
    request: SignRequest,
    config: Optional[SecurityClientConfig] = None,
) -> SignResponse:
    """Sign from a normalized SignRequest."""
    return sign_message(
        message=request.message,
        key_id=request.key_id,
        signing_algorithm=request.signing_algorithm,
        message_type=request.message_type,
        config=config,
    )


def verify_from_request(
    request: VerifyRequest,
    config: Optional[SecurityClientConfig] = None,
) -> VerifyResponse:
    """Verify from a normalized VerifyRequest."""
    return verify_signature(
        message=request.message,
        signature=request.signature,
        key_id=request.key_id,
        signing_algorithm=request.signing_algorithm,
        message_type=request.message_type,
        config=config,
    )


if __name__ == "__main__":
    key_id = os.environ.get("KMS_SIGNING_KEY_ID", "alias/signing-key")
    message = os.environ.get("SIGN_MESSAGE", "message-to-sign-for-verification")

    sign_resp = sign_message(message, key_id)
    print(f"Signature (first 64 chars): {sign_resp.signature[:64]}...")
    print(f"Algorithm: {sign_resp.signing_algorithm}")
    print(f"Key ID: {sign_resp.key_id}")

    verify_resp = verify_signature(message, sign_resp.signature, key_id)
    print(f"Signature valid: {verify_resp.is_valid}")
