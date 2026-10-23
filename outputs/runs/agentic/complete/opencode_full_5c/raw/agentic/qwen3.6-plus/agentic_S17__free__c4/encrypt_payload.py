import os
from typing import Optional, Dict

from security_client import SecurityClient, KMSConfig
from security_models import (
    EncryptionRequest,
    EncryptionResponse,
    EncryptionAlgorithm,
    normalize_payload,
)

AWS_KMS_SERVICE_NAME = "kms"
AWS_KMS_ENDPOINT_HOST = "kms.{region}.amazonaws.com"


def encrypt_payload(
    plaintext: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    config: Optional[KMSConfig] = None,
) -> EncryptionResponse:
    client = SecurityClient(config=config)
    actual_key_id = key_id or client.config.kms_key_id
    if not actual_key_id:
        raise ValueError(
            "No KMS key ID provided. Set AWS_KMS_KEY_ID or pass key_id parameter."
        )

    normalized_plaintext = normalize_payload(plaintext)

    request = EncryptionRequest(
        plaintext=normalized_plaintext,
        key_id=actual_key_id,
        encryption_context=client.normalize_encryption_context(encryption_context),
        encryption_algorithm=EncryptionAlgorithm.SYMMETRIC_DEFAULT,
    )

    response = client.encrypt(request)
    return response


def encrypt_payload_with_context(
    plaintext: str,
    key_id: str,
    context: Dict[str, str],
    algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT,
) -> EncryptionResponse:
    client = SecurityClient()

    request = EncryptionRequest(
        plaintext=normalize_payload(plaintext),
        key_id=key_id,
        encryption_context=context,
        encryption_algorithm=algorithm,
    )

    return client.encrypt(request)


def encrypt_payload_batch(
    payloads: list,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
) -> list:
    client = SecurityClient()
    actual_key_id = key_id or client.config.kms_key_id
    results = []

    for payload in payloads:
        request = EncryptionRequest(
            plaintext=normalize_payload(payload),
            key_id=actual_key_id,
            encryption_context=client.normalize_encryption_context(encryption_context),
            encryption_algorithm=EncryptionAlgorithm.SYMMETRIC_DEFAULT,
        )
        response = client.encrypt(request)
        results.append(response)

    return results
