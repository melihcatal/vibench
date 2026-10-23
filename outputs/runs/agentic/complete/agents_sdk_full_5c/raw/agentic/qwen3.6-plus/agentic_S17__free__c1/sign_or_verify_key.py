"""
sign_or_verify_key.py - Uses AWS KMS for signing and signature verification.

Uses the AWS Key Management Service (KMS) Sign and Verify APIs with asymmetric
KMS keys to create and validate digital signatures. Supports RSASSA_PKCS1_V1_5_SHA_256
and ECDSA_SHA_256 signing algorithms.

Provider: AWS KMS (boto3 client for kms.us-east-1.amazonaws.com)
Key Types: RSA_2048, RSA_3072, RSA_4096, ECC_NIST_P256, ECC_NIST_P384
Signing Algorithms: RSASSA_PKCS1_V1_5_SHA_256, ECDSA_SHA_256
"""

import json
import logging
import sys
from typing import Optional

from security_client import get_kms_client, validate_key_id
from security_models import (
    SigningRequest,
    SigningResponse,
    VerificationRequest,
    VerificationResponse,
    encode_ciphertext,
    normalize_signing_response,
)

logger = logging.getLogger(__name__)

DEFAULT_SIGNING_ALGORITHM = "RSASSA_PKCS1_V1_5_SHA_256"
DEFAULT_VERIFY_ALGORITHM = "RSASSA_PKCS1_V1_5_SHA_256"
DEFAULT_MESSAGE_TYPE = "RAW"


def sign_message(
    message: str,
    key_id: str,
    algorithm: str = DEFAULT_SIGNING_ALGORITHM,
    message_type: str = DEFAULT_MESSAGE_TYPE,
    region: Optional[str] = None,
) -> SigningResponse:
    """
    Sign a message using AWS KMS Sign API with an asymmetric KMS key.

    Args:
        message: The message string to sign.
        key_id: The KMS asymmetric key ID, ARN, or alias.
        algorithm: Signing algorithm (e.g., RSASSA_PKCS1_V1_5_SHA_256, ECDSA_SHA_256).
        message_type: RAW or DIGEST.
        region: AWS region override.

    Returns:
        SigningResponse with base64-encoded signature.

    Raises:
        RuntimeError: If KMS signing fails.
    """
    validate_key_id(key_id)
    kms_client = get_kms_client(region_name=region)

    sign_kwargs = {
        "KeyId": key_id,
        "Message": message.encode("utf-8"),
        "SigningAlgorithm": algorithm,
        "MessageType": message_type,
    }

    try:
        raw_response = kms_client.sign(**sign_kwargs)
    except Exception as e:
        raise RuntimeError(f"AWS KMS Sign failed: {e}") from e

    response = normalize_signing_response(raw_response)
    logger.info(
        "Signed message with KMS key %s using %s",
        response.key_id,
        response.signing_algorithm,
    )
    return response


def verify_signature(
    message: str,
    signature: str,
    key_id: str,
    algorithm: str = DEFAULT_VERIFY_ALGORITHM,
    message_type: str = DEFAULT_MESSAGE_TYPE,
    region: Optional[str] = None,
) -> VerificationResponse:
    """
    Verify a signature using AWS KMS Verify API with an asymmetric KMS key.

    Args:
        message: The original message that was signed.
        signature: Base64-encoded signature to verify.
        key_id: The KMS asymmetric public key ID, ARN, or alias.
        algorithm: Verification algorithm matching the signing algorithm.
        message_type: RAW or DIGEST.
        region: AWS region override.

    Returns:
        VerificationResponse indicating whether the signature is valid.

    Raises:
        RuntimeError: If KMS verification call fails.
    """
    validate_key_id(key_id)
    kms_client = get_kms_client(region_name=region)

    from security_models import decode_ciphertext
    signature_bytes = decode_ciphertext(signature)

    verify_kwargs = {
        "KeyId": key_id,
        "Message": message.encode("utf-8"),
        "Signature": signature_bytes,
        "SigningAlgorithm": algorithm,
        "MessageType": message_type,
    }

    try:
        raw_response = kms_client.verify(**verify_kwargs)
        is_valid = raw_response.get("SignatureValid", False)
    except Exception as e:
        error_msg = str(e).lower()
        if "invalidsignature" in error_msg or "verification failed" in error_msg:
            is_valid = False
        else:
            raise RuntimeError(f"AWS KMS Verify failed: {e}") from e

    response = VerificationResponse(
        is_valid=is_valid,
        key_id=key_id,
    )
    logger.info(
        "Verified signature with KMS key %s: %s",
        key_id,
        "VALID" if is_valid else "INVALID",
    )
    return response


def main():
    """CLI entry point for sign_or_verify_key."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python sign_or_verify_key.py sign <key_id> <message> [algorithm]")
        print("  python sign_or_verify_key.py verify <key_id> <message> <signature_b64> [algorithm]")
        sys.exit(1)

    action = sys.argv[1].lower()
    logging.basicConfig(level=logging.INFO)

    if action == "sign":
        if len(sys.argv) < 4:
            print("Usage: python sign_or_verify_key.py sign <key_id> <message> [algorithm]")
            sys.exit(1)
        key_id = sys.argv[2]
        message = sys.argv[3]
        algo = sys.argv[4] if len(sys.argv) > 4 else DEFAULT_SIGNING_ALGORITHM
        result = sign_message(message, key_id, algorithm=algo)
        output = {
            "action": "sign",
            "signature": result.signature,
            "key_id": result.key_id,
            "algorithm": result.signing_algorithm,
        }
        print(json.dumps(output, indent=2))

    elif action == "verify":
        if len(sys.argv) < 5:
            print("Usage: python sign_or_verify_key.py verify <key_id> <message> <signature> [algorithm]")
            sys.exit(1)
        key_id = sys.argv[2]
        message = sys.argv[3]
        signature = sys.argv[4]
        algo = sys.argv[5] if len(sys.argv) > 5 else DEFAULT_VERIFY_ALGORITHM
        result = verify_signature(message, signature, key_id, algorithm=algo)
        output = {
            "action": "verify",
            "is_valid": result.is_valid,
            "key_id": result.key_id,
            "timestamp": result.timestamp,
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)


if __name__ == "__main__":
    main()
