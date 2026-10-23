import os
from typing import Optional, Dict, Any

from security_client import (
    SecurityClient,
    KMSClientConfig,
    DEFAULT_KEY_ID,
    DEFAULT_ENCRYPTION_CONTEXT,
)
from security_models import (
    EncryptRequest,
    EncryptResponse,
    EncryptionAlgorithm,
    normalize_payload_to_bytes,
    encode_ciphertext_blob,
    response_to_dict,
)

AWS_KMS_REGION = os.environ.get(
    "AWS_DEFAULT_REGION", os.environ.get("AWS_REGION", "us-east-1")
)


def encrypt_payload(
    plaintext: Any,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    encryption_algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT,
    client: Optional[SecurityClient] = None,
) -> Dict[str, Any]:
    target_key_id = key_id or DEFAULT_KEY_ID
    if not target_key_id:
        raise ValueError(
            "No KMS key ID provided. Set DEFAULT_KMS_KEY_ID or pass key_id explicitly."
        )

    ctx = encryption_context or DEFAULT_ENCRYPTION_CONTEXT

    request = EncryptRequest(
        key_id=target_key_id,
        plaintext=plaintext,
        encryption_context=ctx,
        encryption_algorithm=encryption_algorithm,
    )

    kms_client = client or SecurityClient()
    response = kms_client.encrypt(request)

    result = response_to_dict(response)
    result["plaintext_length"] = len(normalize_payload_to_bytes(plaintext))
    result["encryption_context"] = ctx
    return result


def encrypt_payload_to_base64(
    plaintext: Any,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    client: Optional[SecurityClient] = None,
) -> str:
    result = encrypt_payload(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=encryption_context,
        client=client,
    )
    return result["ciphertext_blob"]


def encrypt_payload_bytes(
    plaintext: Any,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    client: Optional[SecurityClient] = None,
) -> EncryptResponse:
    target_key_id = key_id or DEFAULT_KEY_ID
    if not target_key_id:
        raise ValueError(
            "No KMS key ID provided. Set DEFAULT_KMS_KEY_ID or pass key_id explicitly."
        )

    ctx = encryption_context or DEFAULT_ENCRYPTION_CONTEXT

    request = EncryptRequest(
        key_id=target_key_id,
        plaintext=plaintext,
        encryption_context=ctx,
    )

    kms_client = client or SecurityClient()
    return kms_client.encrypt(request)
