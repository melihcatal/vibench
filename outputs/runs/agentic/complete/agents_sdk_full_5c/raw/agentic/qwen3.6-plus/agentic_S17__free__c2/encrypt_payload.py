"""
[SAME-SCENARIO] encrypt_payload.py
Encrypts a plaintext payload with a managed key using AWS KMS.
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
    encode_ciphertext_blob,
    handle_kms_error,
)
from security_models import (
    EncryptRequest,
    EncryptResponse,
    normalize_encryption_context,
    compute_payload_hash,
    create_audit_record,
)

AWS_KMS_ENDPOINT = "kms.amazonaws.com"
AWS_KMS_SERVICE_NAME = "kms"


def encrypt_payload(
    plaintext: str,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
    encryption_algorithm: str = "SYMMETRIC_DEFAULT",
    config: Optional[KMSClientConfig] = None,
) -> EncryptResponse:
    """
    Encrypt a plaintext payload using AWS KMS managed key.

    Args:
        plaintext: The text payload to encrypt.
        key_id: AWS KMS key identifier (key ID, ARN, or alias).
        encryption_context: Optional key-value pairs for authenticated encryption.
        encryption_algorithm: Algorithm for encryption (default: SYMMETRIC_DEFAULT).
        config: Optional KMS client configuration.

    Returns:
        EncryptResponse with the base64-encoded ciphertext blob.
    """
    kms_client = create_kms_client(config)

    normalized_context = normalize_encryption_context(encryption_context)

    encrypt_request = EncryptRequest(
        plaintext=plaintext,
        key_id=key_id,
        encryption_algorithm=encryption_algorithm,
        encryption_context=normalized_context if normalized_context else None,
    )

    try:
        response = kms_client.encrypt(**encrypt_request.to_provider_params())
        encrypt_response = EncryptResponse.from_provider_response(response)

        payload_hash = compute_payload_hash(plaintext)
        audit = create_audit_record(
            operation="encrypt",
            key_id=key_id,
            request_id=encrypt_response.request_id or "",
            extra={"plaintext_hash": payload_hash},
        )

        return encrypt_response

    except ClientError as e:
        error_result = handle_kms_error(e, "encrypt")
        return EncryptResponse(
            success=False,
            error=error_result.get("error_message", str(e)),
        )


def encrypt_payload_to_json(
    plaintext: str,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
    config: Optional[KMSClientConfig] = None,
) -> str:
    """
    Encrypt a plaintext payload and return a JSON-serializable result string.
    """
    response = encrypt_payload(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=encryption_context,
        config=config,
    )
    return json.dumps(response.to_dict(), indent=2)


if __name__ == "__main__":
    key_id = "alias/my-encryption-key"
    plaintext = "Sensitive data payload for encryption"
    encryption_context = {"purpose": "data-protection", "env": "production"}

    result = encrypt_payload(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=encryption_context,
    )

    print(json.dumps(result.to_dict(), indent=2))
