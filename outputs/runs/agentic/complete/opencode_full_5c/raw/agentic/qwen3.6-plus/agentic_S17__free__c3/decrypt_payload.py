import os
from typing import Any, Dict, List, Optional

from security_client import AWS_KMS_KEY_ID, create_kms_client, load_config_from_env
from security_models import (
    DecryptionRequest,
    DecryptionResponse,
    normalize_payload,
    serialize_response,
)


def decrypt_payload(
    ciphertext_blob: str,
    encryption_context: Optional[Dict[str, str]] = None,
    key_id: Optional[str] = None,
) -> DecryptionResponse:
    config = load_config_from_env()
    client = create_kms_client(region=config.get("aws_default_region"))

    request = DecryptionRequest(
        ciphertext_blob=ciphertext_blob,
        encryption_context=encryption_context,
    )

    response = client.decrypt(request)
    return response


def decrypt_and_return_plaintext(
    ciphertext_blob: str,
    encryption_context: Optional[Dict[str, str]] = None,
) -> str:
    response = decrypt_payload(
        ciphertext_blob=ciphertext_blob,
        encryption_context=encryption_context,
    )
    return response.plaintext


def decrypt_and_serialize(
    ciphertext_blob: str,
    encryption_context: Optional[Dict[str, str]] = None,
) -> str:
    response = decrypt_payload(
        ciphertext_blob=ciphertext_blob,
        encryption_context=encryption_context,
    )
    return serialize_response(response)


def batch_decrypt_payloads(
    ciphertext_blobs: Dict[str, str],
    encryption_context: Optional[Dict[str, str]] = None,
) -> Dict[str, Dict[str, Any]]:
    results = {}
    for blob_id, ciphertext in ciphertext_blobs.items():
        try:
            response = decrypt_payload(
                ciphertext_blob=ciphertext,
                encryption_context=encryption_context,
            )
            results[blob_id] = {
                "status": "success",
                "plaintext": response.plaintext,
                "key_id": response.key_id,
                "request_id": response.request_id,
            }
        except Exception as e:
            results[blob_id] = {
                "status": "error",
                "error": str(e),
            }
    return results


def decrypt_multiple(
    ciphertext_blobs: List[str],
    encryption_context: Optional[Dict[str, str]] = None,
) -> List[DecryptionResponse]:
    responses = []
    for ciphertext in ciphertext_blobs:
        response = decrypt_payload(
            ciphertext_blob=ciphertext,
            encryption_context=encryption_context,
        )
        responses.append(response)
    return responses
