"""
[SAME-SCENARIO] sign_or_verify_key.py

Uses AWS Key Management Service (KMS) for signing or signature verification
with asymmetric signing keys.
Provider: AWS KMS | SDK: boto3 | Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

Supports:
- Sign: AWS KMS Sign API with algorithms like RSASSA_PKCS1_V1_5_SHA_256,
  RSASSA_PSS_SHA_256, ECDSA_SHA_256, etc.
- Verify: AWS KMS Verify API to validate a signature against a message.
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
    SignRequest,
    SignResponse,
    VerifyRequest,
    VerifyResponse,
    normalize_kms_response,
)

logger = logging.getLogger(__name__)

# Default signing algorithm for AWS KMS asymmetric keys
DEFAULT_SIGNING_ALGORITHM = "RSASSA_PKCS1_V1_5_SHA_256"


def sign_message(
    message: bytes,
    key_id: Optional[str] = None,
    signing_algorithm: str = DEFAULT_SIGNING_ALGORITHM,
    message_type: str = "RAW",
) -> SignResponse:
    """
    Sign a message using an asymmetric key in AWS KMS.

    Args:
        message: Raw bytes to sign.
        key_id: KMS asymmetric key ID or ARN. Defaults to AWS_KMS_KEY_ID env var.
        signing_algorithm: AWS KMS signing algorithm string.
        message_type: RAW for direct message, DIGEST if message is already hashed.

    Returns:
        SignResponse containing the signature bytes and metadata.

    Raises:
        KMSError: If the KMS sign operation fails.
    """
    kms_client = get_default_kms_client()
    resolved_key_id = key_id or get_kms_key_id()

    if not resolved_key_id:
        raise KMSError(
            "No KMS key ID provided. Set AWS_KMS_KEY_ID or pass key_id explicitly."
        )

    sign_kwargs = {
        "KeyId": resolved_key_id,
        "Message": message,
        "MessageType": message_type,
        "SigningAlgorithm": signing_algorithm,
    }

    try:
        response = kms_client.sign(**sign_kwargs)
    except ClientError as exc:
        raise handle_kms_error(exc, "sign_message") from exc

    norm = normalize_kms_response(response)

    return SignResponse(
        signature=response["Signature"],
        key_id=norm.get("key_id", resolved_key_id),
        signing_algorithm=response.get("SigningAlgorithm", signing_algorithm),
        request_id=norm.get("request_id"),
        metadata=norm.get("metadata", {}),
    )


def verify_signature(
    message: bytes,
    signature: bytes,
    key_id: Optional[str] = None,
    signing_algorithm: str = DEFAULT_SIGNING_ALGORITHM,
    message_type: str = "RAW",
) -> VerifyResponse:
    """
    Verify a signature using an asymmetric key in AWS KMS.

    Args:
        message: Raw bytes that were signed.
        signature: Raw signature bytes to verify.
        key_id: KMS asymmetric key ID or ARN. Defaults to AWS_KMS_KEY_ID env var.
        signing_algorithm: AWS KMS signing algorithm string.
        message_type: RAW for direct message, DIGEST if message is already hashed.

    Returns:
        VerifyResponse indicating whether the signature is valid.

    Raises:
        KMSError: If the KMS verify operation fails.
    """
    kms_client = get_default_kms_client()
    resolved_key_id = key_id or get_kms_key_id()

    if not resolved_key_id:
        raise KMSError(
            "No KMS key ID provided. Set AWS_KMS_KEY_ID or pass key_id explicitly."
        )

    verify_kwargs = {
        "KeyId": resolved_key_id,
        "Message": message,
        "MessageType": message_type,
        "SigningAlgorithm": signing_algorithm,
        "Signature": signature,
    }

    try:
        response = kms_client.verify(**verify_kwargs)
    except ClientError as exc:
        raise handle_kms_error(exc, "verify_signature") from exc

    norm = normalize_kms_response(response)

    return VerifyResponse(
        signature_valid=response.get("SignatureValid", False),
        key_id=norm.get("key_id", resolved_key_id),
        signing_algorithm=response.get("SigningAlgorithm", signing_algorithm),
        request_id=norm.get("request_id"),
        metadata=norm.get("metadata", {}),
    )


def sign_or_verify(
    action: str,
    message: bytes,
    key_id: Optional[str] = None,
    signing_algorithm: str = DEFAULT_SIGNING_ALGORITHM,
    signature: Optional[bytes] = None,
) -> dict:
    """
    Unified interface to either sign or verify using AWS KMS.

    Args:
        action: 'sign' or 'verify'.
        message: Message bytes.
        key_id: KMS key ID.
        signing_algorithm: Signing algorithm string.
        signature: Required for 'verify' action; signature bytes.

    Returns:
        Dict with operation result.
    """
    action_lower = action.lower()
    if action_lower == "sign":
        resp = sign_message(
            message=message,
            key_id=key_id,
            signing_algorithm=signing_algorithm,
        )
        return {
            "action": "sign",
            "key_id": resp.key_id,
            "signing_algorithm": resp.signing_algorithm,
            "signature_b64": base64_encode_bytes(resp.signature),
            "request_id": resp.request_id,
        }
    elif action_lower == "verify":
        if signature is None:
            raise KMSError("Signature is required for verify action.")
        resp = verify_signature(
            message=message,
            signature=signature,
            key_id=key_id,
            signing_algorithm=signing_algorithm,
        )
        return {
            "action": "verify",
            "key_id": resp.key_id,
            "signing_algorithm": resp.signing_algorithm,
            "signature_valid": resp.signature_valid,
            "request_id": resp.request_id,
        }
    else:
        raise KMSError(f"Unknown action: {action}. Use 'sign' or 'verify'.")


def main() -> None:
    """CLI entry point for signing or verifying."""
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) < 3:
        print("Usage: sign_or_verify_key.py <sign|verify> <message> [signature_b64]", file=sys.stderr)
        sys.exit(1)

    action = sys.argv[1]
    message = sys.argv[2].encode("utf-8")
    signature_b64 = sys.argv[3] if len(sys.argv) > 3 else None

    key_id = os.getenv("AWS_KMS_KEY_ID")
    if not key_id:
        print("Error: AWS_KMS_KEY_ID not set.", file=sys.stderr)
        sys.exit(1)

    try:
        sig_bytes = base64_decode_string(signature_b64) if signature_b64 else None
        result = sign_or_verify(
            action=action,
            message=message,
            key_id=key_id,
            signature=sig_bytes,
        )
        print(result)
    except KMSError as exc:
        print(f"Operation failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
