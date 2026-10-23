import os
from typing import Optional, Dict, Tuple

from security_client import SecurityClient, KMSConfig
from security_models import (
    SigningRequest,
    SigningResponse,
    VerificationRequest,
    VerificationResponse,
    SigningAlgorithm,
    MessageType,
    normalize_payload,
)

AWS_KMS_SERVICE_NAME = "kms"
AWS_KMS_ENDPOINT_HOST = "kms.{region}.amazonaws.com"


def sign_message(
    message: str,
    key_id: Optional[str] = None,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256,
    encryption_context: Optional[Dict[str, str]] = None,
    config: Optional[KMSConfig] = None,
) -> SigningResponse:
    client = SecurityClient(config=config)
    actual_key_id = key_id or client.config.signing_key_id or client.config.kms_key_id
    if not actual_key_id:
        raise ValueError(
            "No signing key ID provided. Set AWS_KMS_SIGNING_KEY_ID or pass key_id parameter."
        )

    request = SigningRequest(
        message=normalize_payload(message),
        key_id=actual_key_id,
        signing_algorithm=signing_algorithm,
        message_type=MessageType.RAW,
        encryption_context=client.normalize_encryption_context(encryption_context),
    )

    response = client.sign(request)
    return response


def verify_signature(
    message: str,
    signature: str,
    key_id: Optional[str] = None,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256,
    encryption_context: Optional[Dict[str, str]] = None,
    config: Optional[KMSConfig] = None,
) -> VerificationResponse:
    client = SecurityClient(config=config)
    actual_key_id = key_id or client.config.signing_key_id or client.config.kms_key_id
    if not actual_key_id:
        raise ValueError(
            "No signing key ID provided. Set AWS_KMS_SIGNING_KEY_ID or pass key_id parameter."
        )

    request = VerificationRequest(
        message=normalize_payload(message),
        signature=signature,
        key_id=actual_key_id,
        signing_algorithm=signing_algorithm,
        message_type=MessageType.RAW,
        encryption_context=client.normalize_encryption_context(encryption_context),
    )

    response = client.verify(request)
    return response


def sign_and_verify(
    message: str,
    key_id: Optional[str] = None,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256,
    config: Optional[KMSConfig] = None,
) -> Tuple[SigningResponse, VerificationResponse]:
    signing_response = sign_message(
        message=message,
        key_id=key_id,
        signing_algorithm=signing_algorithm,
        config=config,
    )

    verification_response = verify_signature(
        message=message,
        signature=signing_response.get_signature_b64(),
        key_id=key_id,
        signing_algorithm=signing_algorithm,
        config=config,
    )

    return signing_response, verification_response


def sign_message_digest(
    message_digest: bytes,
    key_id: str,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256,
    config: Optional[KMSConfig] = None,
) -> SigningResponse:
    client = SecurityClient(config=config)

    request = SigningRequest(
        message=message_digest,
        key_id=key_id,
        signing_algorithm=signing_algorithm,
        message_type=MessageType.DIGEST,
    )

    return client.sign(request)


def verify_message_digest(
    message_digest: bytes,
    signature: str,
    key_id: str,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256,
    config: Optional[KMSConfig] = None,
) -> VerificationResponse:
    client = SecurityClient(config=config)

    request = VerificationRequest(
        message=message_digest,
        signature=signature,
        key_id=key_id,
        signing_algorithm=signing_algorithm,
        message_type=MessageType.DIGEST,
    )

    return client.verify(request)
