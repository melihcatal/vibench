import os
import logging
from typing import Optional

from security_client import SecurityClient, KMSConfig
from security_models import (
    SignRequest,
    SignResponse,
    VerifyRequest,
    VerifyResponse,
    SigningAlgorithm,
    MessageType,
)

logger = logging.getLogger(__name__)

AWS_KMS_SERVICE = "AWS Key Management Service"
AWS_KMS_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


def sign_message(
    message: str,
    key_id: str,
    signing_algorithm: str = SigningAlgorithm.RSASSA_PSS_SHA_256,
    message_type: str = MessageType.RAW,
    client: Optional[SecurityClient] = None,
) -> SignResponse:
    config = KMSConfig.from_env()
    kms_client = client or SecurityClient(config=config)

    request = SignRequest(
        key_id=key_id,
        message=message,
        signing_algorithm=signing_algorithm,
        message_type=message_type,
    )

    response = kms_client.sign(request)

    logger.info(
        "Signed message with %s key %s using algorithm %s",
        AWS_KMS_SERVICE,
        response.key_id,
        response.signing_algorithm,
    )

    return response


def verify_signature(
    message: str,
    signature: str,
    key_id: str,
    signing_algorithm: str = SigningAlgorithm.RSASSA_PSS_SHA_256,
    message_type: str = MessageType.RAW,
    client: Optional[SecurityClient] = None,
) -> VerifyResponse:
    config = KMSConfig.from_env()
    kms_client = client or SecurityClient(config=config)

    request = VerifyRequest(
        key_id=key_id,
        message=message,
        signature=signature,
        signing_algorithm=signing_algorithm,
        message_type=message_type,
    )

    response = kms_client.verify(request)

    logger.info(
        "Verified signature with %s key %s using algorithm %s: %s",
        AWS_KMS_SERVICE,
        response.key_id,
        response.signing_algorithm,
        response.signature_valid,
    )

    return response


def sign_or_verify(
    action: str,
    message: str,
    key_id: str,
    signature: Optional[str] = None,
    signing_algorithm: str = SigningAlgorithm.RSASSA_PSS_SHA_256,
    message_type: str = MessageType.RAW,
    client: Optional[SecurityClient] = None,
) -> dict:
    if action.lower() == "sign":
        result = sign_message(
            message=message,
            key_id=key_id,
            signing_algorithm=signing_algorithm,
            message_type=message_type,
            client=client,
        )
        return {
            "action": "sign",
            "signature": result.signature,
            "key_id": result.key_id,
            "signing_algorithm": result.signing_algorithm,
        }
    elif action.lower() == "verify":
        if not signature:
            raise ValueError("signature is required for verify action")
        result = verify_signature(
            message=message,
            signature=signature,
            key_id=key_id,
            signing_algorithm=signing_algorithm,
            message_type=message_type,
            client=client,
        )
        return {
            "action": "verify",
            "signature_valid": result.signature_valid,
            "key_id": result.key_id,
            "signing_algorithm": result.signing_algorithm,
        }
    else:
        raise ValueError("action must be 'sign' or 'verify'")
