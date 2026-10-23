import os
from typing import Optional, Dict

from security_client import SecurityClient, KMSConfig
from security_models import (
    DecryptionRequest,
    DecryptionResponse,
    EncryptionAlgorithm,
    normalize_ciphertext,
)

AWS_KMS_SERVICE_NAME = "kms"
AWS_KMS_ENDPOINT_HOST = "kms.{region}.amazonaws.com"


def decrypt_payload(
    ciphertext: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    config: Optional[KMSConfig] = None,
) -> DecryptionResponse:
    client = SecurityClient(config=config)
    actual_key_id = key_id or client.config.kms_key_id

    normalized_ciphertext = normalize_ciphertext(ciphertext)

    request = DecryptionRequest(
        ciphertext_blob=normalized_ciphertext,
        key_id=actual_key_id,
        encryption_context=client.normalize_encryption_context(encryption_context),
    )

    response = client.decrypt(request)
    return response


def decrypt_payload_to_string(
    ciphertext: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
) -> str:
    response = decrypt_payload(
        ciphertext, key_id=key_id, encryption_context=encryption_context
    )
    return response.get_plaintext_str()


def decrypt_payload_batch(
    ciphertexts: list,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
) -> list:
    client = SecurityClient()
    actual_key_id = key_id or client.config.kms_key_id
    results = []

    for ct in ciphertexts:
        request = DecryptionRequest(
            ciphertext_blob=normalize_ciphertext(ct),
            key_id=actual_key_id,
            encryption_context=client.normalize_encryption_context(encryption_context),
        )
        response = client.decrypt(request)
        results.append(response)

    return results


def decrypt_and_verify_context(
    ciphertext: str,
    expected_context: Dict[str, str],
    key_id: Optional[str] = None,
) -> DecryptionResponse:
    response = decrypt_payload(
        ciphertext,
        key_id=key_id,
        encryption_context=expected_context,
    )
    return response
