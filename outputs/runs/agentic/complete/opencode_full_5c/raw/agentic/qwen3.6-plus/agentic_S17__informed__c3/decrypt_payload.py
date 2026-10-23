import os
import logging
from typing import Optional, Dict, List

from security_client import SecurityClient, KMSConfig
from security_models import DecryptRequest, DecryptResponse

logger = logging.getLogger(__name__)

AWS_KMS_SERVICE = "AWS Key Management Service"
AWS_KMS_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


def decrypt_payload(
    ciphertext_blob: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    encryption_algorithm: str = "SYMMETRIC_DEFAULT",
    grant_tokens: Optional[List[str]] = None,
    client: Optional[SecurityClient] = None,
) -> DecryptResponse:
    config = KMSConfig.from_env()
    kms_client = client or SecurityClient(config=config)

    request = DecryptRequest(
        ciphertext_blob=ciphertext_blob,
        encryption_context=encryption_context,
        encryption_algorithm=encryption_algorithm,
        grant_tokens=grant_tokens,
    )

    response = kms_client.decrypt(request)

    logger.info(
        "Decrypted payload with %s key %s using algorithm %s",
        AWS_KMS_SERVICE,
        response.key_id,
        response.encryption_algorithm,
    )

    return response


def decrypt_payload_from_env(
    ciphertext_blob: str,
    encryption_context: Optional[Dict[str, str]] = None,
) -> DecryptResponse:
    key_id = os.environ.get("AWS_KMS_KEY_ID")

    return decrypt_payload(
        ciphertext_blob=ciphertext_blob,
        key_id=key_id,
        encryption_context=encryption_context,
    )
