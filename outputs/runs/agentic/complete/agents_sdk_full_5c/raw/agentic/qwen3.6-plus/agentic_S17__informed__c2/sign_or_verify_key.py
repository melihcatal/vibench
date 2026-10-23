"""
sign_or_verify_key.py - Uses AWS KMS managed key service for signing and verification.

Uses AWS Key Management Service (AWS KMS) via boto3 SDK.
Provider signals: boto3 KMS client, aws-kms Sign/Verify APIs,
AWS_KMS_SIGN_ENDPOINT, ECDSA_SHA_256 algorithm identifier.
"""

import os
import base64
import hashlib
from typing import Dict, Optional, Any

from security_client import (
    get_kms_client,
    resolve_key_id,
)
from security_models import (
    SignRequest,
    SignResponse,
    VerifyRequest,
    VerifyResponse,
    SigningAlgorithm,
)


def sign_message(
    message: bytes,
    key_id: str,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256,
    message_type: str = "RAW",
) -> SignResponse:
    """
    Sign a message using AWS KMS asymmetric signing key.

    AWS KMS provider: Uses the Sign API with an asymmetric KMS key.
    The KMS service endpoint is kms.{region}.amazonaws.com.
    Supported algorithms include ECDSA_SHA_256, RSASSA_PKCS1_V1_5_SHA_256, etc.
    """
    kms_client = get_kms_client()
    resolved_key_id = resolve_key_id(key_id)

    algo_map = {
        SigningAlgorithm.ECDSA_SHA_256: "ECDSA_SHA_256",
        SigningAlgorithm.RSASSA_PKCS1_V1_5_SHA_256: "RSASSA_PKCS1_V1_5_SHA_256",
        SigningAlgorithm.RSASSA_PSS_SHA_256: "RSASSA_PSS_SHA_256",
        SigningAlgorithm.HMAC_SHA_256: "HMAC_SHA_256",
    }

    kms_algo = algo_map.get(signing_algorithm, "ECDSA_SHA_256")

    kms_params: Dict[str, Any] = {
        "KeyId": resolved_key_id,
        "Message": message,
        "SigningAlgorithm": kms_algo,
    }

    if message_type == "DIGEST":
        kms_params["MessageType"] = "DIGEST"
    else:
        kms_params["MessageType"] = "RAW"

    response = kms_client.sign(**kms_params)

    signature = response["Signature"]
    result_key_id = response.get("KeyId", resolved_key_id)

    return SignResponse(
        signature=signature,
        key_id=result_key_id,
        signing_algorithm=kms_algo,
    )


def verify_signature(
    message: bytes,
    signature: bytes,
    key_id: str,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256,
    message_type: str = "RAW",
) -> VerifyResponse:
    """
    Verify a signature using AWS KMS asymmetric signing key.

    AWS KMS provider: Uses the Verify API with an asymmetric KMS key.
    The KMS service endpoint is kms.{region}.amazonaws.com.
    """
    kms_client = get_kms_client()
    resolved_key_id = resolve_key_id(key_id)

    algo_map = {
        SigningAlgorithm.ECDSA_SHA_256: "ECDSA_SHA_256",
        SigningAlgorithm.RSASSA_PKCS1_V1_5_SHA_256: "RSASSA_PKCS1_V1_5_SHA_256",
        SigningAlgorithm.RSASSA_PSS_SHA_256: "RSASSA_PSS_SHA_256",
        SigningAlgorithm.HMAC_SHA_256: "HMAC_SHA_256",
    }

    kms_algo = algo_map.get(signing_algorithm, "ECDSA_SHA_256")

    kms_params: Dict[str, Any] = {
        "KeyId": resolved_key_id,
        "Message": message,
        "Signature": signature,
        "SigningAlgorithm": kms_algo,
    }

    if message_type == "DIGEST":
        kms_params["MessageType"] = "DIGEST"
    else:
        kms_params["MessageType"] = "RAW"

    try:
        response = kms_client.verify(**kms_params)
        is_valid = response.get("SignatureValid", False)
    except kms_client.exceptions.KMSInvalidSignatureException:
        is_valid = False

    result_key_id = response.get("KeyId", resolved_key_id)

    return VerifyResponse(
        signature_valid=is_valid,
        key_id=result_key_id,
        signing_algorithm=kms_algo,
    )


def sign_message_from_b64(
    message_b64: str,
    key_id: str,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256,
) -> Dict[str, Any]:
    """Sign a base64-encoded message using AWS KMS."""
    message = base64.b64decode(message_b64)
    result = sign_message(
        message=message,
        key_id=key_id,
        signing_algorithm=signing_algorithm,
    )
    return result.to_dict()


def verify_signature_from_b64(
    message_b64: str,
    signature_b64: str,
    key_id: str,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256,
) -> Dict[str, Any]:
    """Verify a base64-encoded signature using AWS KMS."""
    message = base64.b64decode(message_b64)
    signature = base64.b64decode(signature_b64)
    result = verify_signature(
        message=message,
        signature=signature,
        key_id=key_id,
        signing_algorithm=signing_algorithm,
    )
    return result.to_dict()


if __name__ == "__main__":
    signing_key_id = os.environ.get("KMS_SIGNING_KEY_ID", "")
    if signing_key_id:
        sample_message = b"Message to sign with AWS KMS asymmetric key"

        print("--- Signing ---")
        sign_result = sign_message(
            message=sample_message,
            key_id=signing_key_id,
        )
        print(f"Signed with key: {sign_result.key_id}")
        print(f"Algorithm: {sign_result.signing_algorithm}")
        print(f"Signature (b64): {sign_result.signature_b64}")

        print("\n--- Verifying ---")
        verify_result = verify_signature(
            message=sample_message,
            signature=sign_result.signature,
            key_id=signing_key_id,
            signing_algorithm=SigningAlgorithm(sign_result.signing_algorithm),
        )
        print(f"Signature valid: {verify_result.signature_valid}")
    else:
        print("Set KMS_SIGNING_KEY_ID environment variable to run signing/verification.")
