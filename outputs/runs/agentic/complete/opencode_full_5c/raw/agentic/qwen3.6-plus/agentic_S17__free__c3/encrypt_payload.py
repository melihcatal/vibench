import os
from typing import Any, Dict, Optional

from security_client import AWS_KMS_KEY_ID, create_kms_client, load_config_from_env
from security_models import (
    EncryptionAlgorithm,
    EncryptionRequest,
    EncryptionResponse,
    normalize_payload,
    serialize_response,
)


def encrypt_payload(
    plaintext: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT,
) -> EncryptionResponse:
    config = load_config_from_env()
    client = create_kms_client(region=config.get("aws_default_region"))

    resolved_key_id = key_id or os.environ.get("AWS_KMS_KEY_ID", "")
    if not resolved_key_id:
        raise ValueError(
            "AWS_KMS_KEY_ID environment variable or key_id parameter is required"
        )

    normalized = normalize_payload(plaintext)

    request = EncryptionRequest(
        key_id=resolved_key_id,
        plaintext=normalized,
        encryption_context=encryption_context,
        encryption_algorithm=algorithm,
    )

    response = client.encrypt(request)
    return response


def encrypt_payload_with_context(
    plaintext: str,
    key_id: str,
    context: Dict[str, str],
    algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT,
) -> EncryptionResponse:
    return encrypt_payload(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=context,
        algorithm=algorithm,
    )


def encrypt_and_serialize(
    plaintext: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
) -> str:
    response = encrypt_payload(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=encryption_context,
    )
    return serialize_response(response)


def batch_encrypt_payloads(
    payloads: Dict[str, str],
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
) -> Dict[str, Dict[str, Any]]:
    results = {}
    for payload_id, plaintext in payloads.items():
        try:
            response = encrypt_payload(
                plaintext=plaintext,
                key_id=key_id,
                encryption_context=encryption_context,
            )
            results[payload_id] = {
                "status": "success",
                "ciphertext_blob": response.ciphertext_blob,
                "key_id": response.key_id,
                "request_id": response.request_id,
            }
        except Exception as e:
            results[payload_id] = {
                "status": "error",
                "error": str(e),
            }
    return results
