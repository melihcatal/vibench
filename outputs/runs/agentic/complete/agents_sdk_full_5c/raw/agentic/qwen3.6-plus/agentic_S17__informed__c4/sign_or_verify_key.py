"""Uses AWS KMS managed key service for signing or verification."""

import base64
from typing import Optional, Dict

from security_client import get_kms_client, ensure_binary
from security_models import (
    SignRequest,
    SignResponse,
    VerifyRequest,
    VerifyResponse,
    normalize_sign_response,
    normalize_verify_response,
)


def sign_message(
    message: bytes,
    key_id: str,
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
    message_type: str = "RAW",
    region: str = "us-east-1",
) -> SignResponse:
    """Sign a message using an AWS KMS asymmetric signing key.

    Args:
        message: The raw message bytes to sign.
        key_id: AWS KMS asymmetric key ID or alias.
        signing_algorithm: KMS signing algorithm (e.g., RSASSA_PKCS1_V1_5_SHA_256,
            ECDSA_SHA_256).
        message_type: Type of message (RAW or DIGEST).
        region: AWS region.

    Returns:
        SignResponse containing the signature and metadata.
    """
    kms = get_kms_client(region=region)
    msg = ensure_binary(message)

    params = {
        "KeyId": key_id,
        "Message": msg,
        "SigningAlgorithm": signing_algorithm,
        "MessageType": message_type,
    }

    response = kms.sign(**params)

    raw = {
        "signature": response["Signature"],
        "key_id": response["KeyId"],
        "signing_algorithm": response["SigningAlgorithm"],
    }
    return normalize_sign_response(raw)


def verify_signature(
    message: bytes,
    signature: bytes,
    key_id: str,
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
    message_type: str = "RAW",
    region: str = "us-east-1",
) -> VerifyResponse:
    """Verify a signature using an AWS KMS asymmetric signing key.

    Args:
        message: The original raw message bytes.
        signature: The signature bytes to verify.
        key_id: AWS KMS asymmetric key ID or alias.
        signing_algorithm: KMS signing algorithm used to create the signature.
        message_type: Type of message (RAW or DIGEST).
        region: AWS region.

    Returns:
        VerifyResponse indicating if the signature is valid.
    """
    kms = get_kms_client(region=region)
    msg = ensure_binary(message)

    params = {
        "KeyId": key_id,
        "Message": msg,
        "Signature": signature,
        "SigningAlgorithm": signing_algorithm,
        "MessageType": message_type,
    }

    response = kms.verify(**params)

    raw = {
        "signature_valid": response["SignatureValid"],
        "key_id": response["KeyId"],
        "signing_algorithm": response["SigningAlgorithm"],
    }
    return normalize_verify_response(raw)


if __name__ == "__main__":
    import os

    message = b"Message to sign with KMS asymmetric key"
    key_id = os.environ.get("AWS_KMS_SIGNING_KEY_ID", "alias/signing-key")
    sign_result = sign_message(message, key_id)
    print(f"Signature (base64): {base64.b64encode(sign_result.signature).decode('utf-8')}")

    verify_result = verify_signature(message, sign_result.signature, key_id)
    print(f"Signature valid: {verify_result.valid}")
