import os
import logging
from typing import Optional, Dict, List

from security_client import SecurityClient, KMSConfig
from security_models import EncryptRequest, EncryptResponse

logger = logging.getLogger(__name__)

AWS_KMS_SERVICE = "AWS Key Management Service"
AWS_KMS_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


def encrypt_payload(
    plaintext: str,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
    encryption_algorithm: str = "SYMMETRIC_DEFAULT",
    grant_tokens: Optional[List[str]] = None,
    client: Optional[SecurityClient] = None,
) -> EncryptResponse:
    config = KMSConfig.from_env()
    kms_client = client or SecurityClient(config=config)

    request = EncryptRequest(
        key_id=key_id,
        plaintext=plaintext,
        encryption_context=encryption_context,
        encryption_algorithm=encryption_algorithm,
        grant_tokens=grant_tokens,
    )

    response = kms_client.encrypt(request)

    logger.info(
        "Encrypted payload with %s key %s using algorithm %s",
        AWS_KMS_SERVICE,
        response.key_id,
        response.encryption_algorithm,
    )

    return response


def encrypt_payload_from_env(
    plaintext: str,
    encryption_context: Optional[Dict[str, str]] = None,
) -> EncryptResponse:
    key_id = os.environ.get("AWS_KMS_KEY_ID")
    if not key_id:
        raise ValueError("AWS_KMS_KEY_ID environment variable is required")

    return encrypt_payload(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=encryption_context,
    )
