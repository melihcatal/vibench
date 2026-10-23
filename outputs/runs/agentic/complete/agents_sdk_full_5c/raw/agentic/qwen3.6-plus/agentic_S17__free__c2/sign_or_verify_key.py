"""
[SAME-SCENARIO] sign_or_verify_key.py
Uses AWS KMS managed key service for signing or verification of messages.
Provider: AWS Key Management Service (kms.amazonaws.com)
Supports RSA and ECDSA signing algorithms via KMS Sign and Verify APIs.
"""

import base64
import json
import sys
from typing import Optional, Dict, Any

from botocore.exceptions import ClientError

from security_client import (
    create_kms_client,
    KMSClientConfig,
    handle_kms_error,
)
from security_models import (
    SignRequest,
    SignResponse,
    VerifyRequest,
    VerifyResponse,
    create_audit_record,
)

AWS_KMS_ENDPOINT = "kms.amazonaws.com"
AWS_KMS_SERVICE_NAME = "kms"


def sign_message(
    message: str,
    key_id: str,
    signing_algorithm: str = "RSASSA_PSS_SHA_256",
    message_type: str = "RAW",
    config: Optional[KMSClientConfig] = None,
) -> SignResponse:
    """
    Sign a message using AWS KMS managed asymmetric key.

    Args:
        message: The message to sign.
        key_id: AWS KMS key identifier for an asymmetric signing key.
        signing_algorithm: Signing algorithm (e.g., RSASSA_PSS_SHA_256, ECDSA_SHA_256).
        message_type: RAW or DIGEST.
        config: Optional KMS client configuration.

    Returns:
        SignResponse with the base64-encoded signature.
    """
    kms_client = create_kms_client(config)

    sign_request = SignRequest(
        message=message,
        key_id=key_id,
        signing_algorithm=signing_algorithm,
        message_type=message_type,
    )

    try:
        response = kms_client.sign(**sign_request.to_provider_params())
        sign_response = SignResponse.from_provider_response(response)

        audit = create_audit_record(
            operation="sign",
            key_id=key_id,
            request_id=sign_response.request_id or "",
            extra={"signing_algorithm": signing_algorithm},
        )

        return sign_response

    except ClientError as e:
        error_result = handle_kms_error(e, "sign")
        return SignResponse(
            success=False,
            error=error_result.get("error_message", str(e)),
        )


def verify_signature(
    message: str,
    signature_b64: str,
    key_id: str,
    signing_algorithm: str = "RSASSA_PSS_SHA_256",
    message_type: str = "RAW",
    config: Optional[KMSClientConfig] = None,
) -> VerifyResponse:
    """
    Verify a signature using AWS KMS managed asymmetric key.

    Args:
        message: The original message that was signed.
        signature_b64: Base64-encoded signature to verify.
        key_id: AWS KMS key identifier used for signing.
        signing_algorithm: Signing algorithm used.
        message_type: RAW or DIGEST.
        config: Optional KMS client configuration.

    Returns:
        VerifyResponse indicating whether the signature is valid.
    """
    kms_client = create_kms_client(config)
    signature_bytes = base64.b64decode(signature_b64)

    verify_request = VerifyRequest(
        message=message,
        signature=signature_bytes,
        key_id=key_id,
        signing_algorithm=signing_algorithm,
        message_type=message_type,
    )

    try:
        response = kms_client.verify(**verify_request.to_provider_params())
        verify_response = VerifyResponse.from_provider_response(response)

        audit = create_audit_record(
            operation="verify",
            key_id=key_id,
            request_id=verify_response.request_id or "",
            extra={
                "signing_algorithm": signing_algorithm,
                "signature_valid": verify_response.signature_valid,
            },
        )

        return verify_response

    except ClientError as e:
        error_result = handle_kms_error(e, "verify")
        return VerifyResponse(
            success=False,
            error=error_result.get("error_message", str(e)),
        )


def sign_and_verify(
    message: str,
    key_id: str,
    signing_algorithm: str = "RSASSA_PSS_SHA_256",
    config: Optional[KMSClientConfig] = None,
) -> Dict[str, Any]:
    """
    Sign a message and then verify the signature as a combined operation.
    Demonstrates the full sign/verify workflow with AWS KMS.
    """
    sign_result = sign_message(
        message=message,
        key_id=key_id,
        signing_algorithm=signing_algorithm,
        config=config,
    )

    if not sign_result.success:
        return {
            "success": False,
            "sign_error": sign_result.error,
            "provider": "aws-kms",
            "endpoint": AWS_KMS_ENDPOINT,
        }

    verify_result = verify_signature(
        message=message,
        signature_b64=sign_result.signature,
        key_id=key_id,
        signing_algorithm=signing_algorithm,
        config=config,
    )

    return {
        "success": verify_result.success and verify_result.signature_valid,
        "signature": sign_result.signature,
        "signature_valid": verify_result.signature_valid,
        "key_id": key_id,
        "signing_algorithm": signing_algorithm,
        "provider": "aws-kms",
        "endpoint": AWS_KMS_ENDPOINT,
        "sign_request_id": sign_result.request_id,
        "verify_request_id": verify_result.request_id,
    }


def sign_or_verify_to_json(
    operation: str,
    message: str,
    key_id: str,
    signature_b64: Optional[str] = None,
    signing_algorithm: str = "RSASSA_PSS_SHA_256",
    config: Optional[KMSClientConfig] = None,
) -> str:
    """
    Perform sign or verify operation and return JSON result.
    """
    if operation.lower() == "sign":
        result = sign_message(
            message=message,
            key_id=key_id,
            signing_algorithm=signing_algorithm,
            config=config,
        )
    elif operation.lower() == "verify":
        if not signature_b64:
            return json.dumps({"success": False, "error": "signature_b64 required for verify"})
        result = verify_signature(
            message=message,
            signature_b64=signature_b64,
            key_id=key_id,
            signing_algorithm=signing_algorithm,
            config=config,
        )
    else:
        return json.dumps({"success": False, "error": "operation must be 'sign' or 'verify'"})

    return json.dumps(result.to_dict(), indent=2)


if __name__ == "__main__":
    key_id = "alias/my-signing-key"
    message = "This message requires a cryptographic signature"

    result = sign_and_verify(
        message=message,
        key_id=key_id,
        signing_algorithm="RSASSA_PSS_SHA_256",
    )

    print(json.dumps(result, indent=2))
