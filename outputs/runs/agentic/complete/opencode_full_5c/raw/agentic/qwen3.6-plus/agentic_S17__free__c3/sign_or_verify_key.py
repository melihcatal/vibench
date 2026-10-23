import os
from typing import Any, Dict, Optional

from security_client import AWS_KMS_KEY_ID, create_kms_client, load_config_from_env
from security_models import (
    SigningAlgorithm,
    SigningRequest,
    SigningResponse,
    VerificationRequest,
    VerificationResponse,
    normalize_payload,
    serialize_response,
)


def sign_message(
    message: str,
    key_id: Optional[str] = None,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256,
    encryption_context: Optional[Dict[str, str]] = None,
) -> SigningResponse:
    config = load_config_from_env()
    client = create_kms_client(region=config.get("aws_default_region"))

    resolved_key_id = key_id or os.environ.get(
        "AWS_KMS_SIGNING_KEY_ID", os.environ.get("AWS_KMS_KEY_ID", "")
    )
    if not resolved_key_id:
        raise ValueError(
            "AWS_KMS_SIGNING_KEY_ID or AWS_KMS_KEY_ID environment variable or key_id parameter is required"
        )

    normalized = normalize_payload(message)

    request = SigningRequest(
        key_id=resolved_key_id,
        message=normalized,
        signing_algorithm=signing_algorithm,
        encryption_context=encryption_context,
    )

    response = client.sign(request)
    return response


def verify_signature(
    message: str,
    signature: str,
    key_id: Optional[str] = None,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256,
    encryption_context: Optional[Dict[str, str]] = None,
) -> VerificationResponse:
    config = load_config_from_env()
    client = create_kms_client(region=config.get("aws_default_region"))

    resolved_key_id = key_id or os.environ.get(
        "AWS_KMS_SIGNING_KEY_ID", os.environ.get("AWS_KMS_KEY_ID", "")
    )
    if not resolved_key_id:
        raise ValueError(
            "AWS_KMS_SIGNING_KEY_ID or AWS_KMS_KEY_ID environment variable or key_id parameter is required"
        )

    normalized = normalize_payload(message)

    request = VerificationRequest(
        key_id=resolved_key_id,
        message=normalized,
        signature=signature,
        signing_algorithm=signing_algorithm,
        encryption_context=encryption_context,
    )

    response = client.verify(request)
    return response


def sign_and_serialize(
    message: str,
    key_id: Optional[str] = None,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256,
) -> str:
    response = sign_message(
        message=message,
        key_id=key_id,
        signing_algorithm=signing_algorithm,
    )
    return serialize_response(response)


def verify_and_return_result(
    message: str,
    signature: str,
    key_id: Optional[str] = None,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256,
) -> bool:
    response = verify_signature(
        message=message,
        signature=signature,
        key_id=key_id,
        signing_algorithm=signing_algorithm,
    )
    return response.signature_valid


def sign_with_context(
    message: str,
    key_id: str,
    context: Dict[str, str],
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256,
) -> SigningResponse:
    return sign_message(
        message=message,
        key_id=key_id,
        signing_algorithm=signing_algorithm,
        encryption_context=context,
    )


def verify_with_context(
    message: str,
    signature: str,
    key_id: str,
    context: Dict[str, str],
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256,
) -> VerificationResponse:
    return verify_signature(
        message=message,
        signature=signature,
        key_id=key_id,
        signing_algorithm=signing_algorithm,
        encryption_context=context,
    )


def sign_and_verify_roundtrip(
    message: str,
    key_id: Optional[str] = None,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256,
) -> Dict[str, Any]:
    sign_response = sign_message(
        message=message,
        key_id=key_id,
        signing_algorithm=signing_algorithm,
    )

    verify_response = verify_signature(
        message=message,
        signature=sign_response.signature,
        key_id=key_id,
        signing_algorithm=signing_algorithm,
    )

    return {
        "signature": sign_response.signature,
        "signature_valid": verify_response.signature_valid,
        "sign_request_id": sign_response.request_id,
        "verify_request_id": verify_response.request_id,
        "key_id": sign_response.key_id,
        "signing_algorithm": sign_response.signing_algorithm,
    }
