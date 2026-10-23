"""
[SAME-SCENARIO] decrypt_payload.py
Decrypts a ciphertext payload with a managed key using AWS KMS.
Provider: AWS Key Management Service (kms.amazonaws.com)
"""

import base64
import json
import sys
from typing import Optional, Dict, Any

from botocore.exceptions import ClientError

from security_client import (
    create_kms_client,
    KMSClientConfig,
    decode_ciphertext_blob,
    handle_kms_error,
)
from security_models import (
    DecryptRequest,
    DecryptResponse,
    normalize_encryption_context,
    create_audit_record,
)

AWS_KMS_ENDPOINT = "kms.amazonaws.com"
AWS_KMS_SERVICE_NAME = "kms"


def decrypt_payload(
    ciphertext_blob_b64: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    config: Optional[KMSClientConfig] = None,
) -> DecryptResponse:
    """
    Decrypt a ciphertext payload using AWS KMS managed key.

    Args:
        ciphertext_blob_b64: Base64-encoded ciphertext blob from KMS.
        key_id: Optional key identifier for disambiguation.
        encryption_context: Optional context used during encryption.
        config: Optional KMS client configuration.

    Returns:
        DecryptResponse with the decrypted plaintext string.
    """
    kms_client = create_kms_client(config)

    ciphertext_bytes = decode_ciphertext_blob(ciphertext_blob_b64)
    normalized_context = normalize_encryption_context(encryption_context)

    decrypt_request = DecryptRequest(
        ciphertext_blob=ciphertext_bytes,
        key_id=key_id,
        encryption_context=normalized_context if normalized_context else None,
    )

    try:
        response = kms_client.decrypt(**decrypt_request.to_provider_params())
        decrypt_response = DecryptResponse.from_provider_response(response)

        audit = create_audit_record(
            operation="decrypt",
            key_id=decrypt_response.key_id or key_id or "unknown",
            request_id=decrypt_response.request_id or "",
        )

        return decrypt_response

    except ClientError as e:
        error_result = handle_kms_error(e, "decrypt")
        return DecryptResponse(
            success=False,
            error=error_result.get("error_message", str(e)),
        )


def decrypt_payload_to_json(
    ciphertext_blob_b64: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    config: Optional[KMSClientConfig] = None,
) -> str:
    """
    Decrypt a ciphertext payload and return a JSON-serializable result string.
    """
    response = decrypt_payload(
        ciphertext_blob_b64=ciphertext_blob_b64,
        key_id=key_id,
        encryption_context=encryption_context,
        config=config,
    )
    return json.dumps(response.to_dict(), indent=2)


if __name__ == "__main__":
    sample_ciphertext = (
        "AQICAHh..."
    )

    result = decrypt_payload(
        ciphertext_blob_b64=sample_ciphertext,
        encryption_context={"purpose": "data-protection", "env": "production"},
    )

    print(json.dumps(result.to_dict(), indent=2))
