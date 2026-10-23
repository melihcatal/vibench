import os
from typing import Optional, Dict, Any

from security_client import (
    SecurityClient,
    KMSClientConfig,
    DEFAULT_KEY_ID,
    DEFAULT_ENCRYPTION_CONTEXT,
)
from security_models import (
    DecryptRequest,
    DecryptResponse,
    EncryptionAlgorithm,
    decode_ciphertext_blob,
    response_to_dict,
)

AWS_KMS_REGION = os.environ.get(
    "AWS_DEFAULT_REGION", os.environ.get("AWS_REGION", "us-east-1")
)


def decrypt_payload(
    ciphertext: Any,
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

    if isinstance(ciphertext, str):
        ciphertext_bytes = decode_ciphertext_blob(ciphertext)
    elif isinstance(ciphertext, bytes):
        ciphertext_bytes = ciphertext
    else:
        ciphertext_bytes = bytes(ciphertext)

    request = DecryptRequest(
        ciphertext_blob=ciphertext_bytes,
        encryption_context=ctx,
        encryption_algorithm=encryption_algorithm,
        key_id=target_key_id,
    )

    kms_client = client or SecurityClient()
    response = kms_client.decrypt(request)

    result = response_to_dict(response)
    result["plaintext_decoded"] = response.plaintext.decode("utf-8", errors="replace")
    result["encryption_context"] = ctx
    return result


def decrypt_payload_to_string(
    ciphertext: Any,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    client: Optional[SecurityClient] = None,
) -> str:
    result = decrypt_payload(
        ciphertext=ciphertext,
        key_id=key_id,
        encryption_context=encryption_context,
        client=client,
    )
    return result["plaintext_decoded"]


def decrypt_payload_bytes(
    ciphertext: Any,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    client: Optional[SecurityClient] = None,
) -> DecryptResponse:
    target_key_id = key_id or DEFAULT_KEY_ID
    if not target_key_id:
        raise ValueError(
            "No KMS key ID provided. Set DEFAULT_KMS_KEY_ID or pass key_id explicitly."
        )

    ctx = encryption_context or DEFAULT_ENCRYPTION_CONTEXT

    if isinstance(ciphertext, str):
        ciphertext_bytes = decode_ciphertext_blob(ciphertext)
    elif isinstance(ciphertext, bytes):
        ciphertext_bytes = ciphertext
    else:
        ciphertext_bytes = bytes(ciphertext)

    request = DecryptRequest(
        ciphertext_blob=ciphertext_bytes,
        encryption_context=ctx,
        key_id=target_key_id,
    )

    kms_client = client or SecurityClient()
    return kms_client.decrypt(request)
