"""
decrypt_payload.py - Decrypts a ciphertext payload with an AWS KMS managed key.

Uses AWS Key Management Service (AWS KMS) via boto3 SDK.
Provider signals: boto3 KMS client, AWS_KMS_DECRYPT_ENDPOINT,
aws-kms decryption algorithm identifiers.
"""

import os
import base64
from typing import Dict, Optional, Any

from security_client import (
    get_kms_client,
    build_encryption_context,
    resolve_key_id,
    validate_ciphertext_blob,
)
from security_models import (
    DecryptRequest,
    DecryptResponse,
    normalize_encryption_context,
)


def decrypt_payload(
    ciphertext_blob: bytes,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    grant_tokens: Optional[list] = None,
) -> DecryptResponse:
    """
    Decrypt a ciphertext blob using AWS KMS managed key.

    AWS KMS provider: Uses the Decrypt API. The KMS service endpoint
    is kms.{region}.amazonaws.com. If key_id is embedded in the
    ciphertext blob, AWS KMS derives it automatically.
    """
    kms_client = get_kms_client()

    normalized_context = normalize_encryption_context(encryption_context)

    kms_params: Dict[str, Any] = {
        "CiphertextBlob": ciphertext_blob,
    }

    if key_id:
        kms_params["KeyId"] = resolve_key_id(key_id)

    if normalized_context:
        kms_params["EncryptionContext"] = normalized_context

    if grant_tokens:
        kms_params["GrantTokens"] = grant_tokens

    response = kms_client.decrypt(**kms_params)

    plaintext = response["Plaintext"]
    result_key_id = response.get("KeyId", key_id or "unknown")
    encryption_algo = response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT")

    return DecryptResponse(
        plaintext=plaintext,
        key_id=result_key_id,
        encryption_algorithm=encryption_algo,
    )


def decrypt_payload_from_b64(
    ciphertext_b64: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Decrypt a base64-encoded ciphertext blob and return a dict result."""
    ciphertext_blob = validate_ciphertext_blob(ciphertext_b64)
    result = decrypt_payload(
        ciphertext_blob=ciphertext_blob,
        key_id=key_id,
        encryption_context=encryption_context,
    )
    return result.to_dict()


if __name__ == "__main__":
    key_id = os.environ.get("KMS_KEY_ID", "")
    ciphertext_b64 = os.environ.get("KMS_CIPHERTEXT_B64", "")

    if ciphertext_b64:
        response = decrypt_payload_from_b64(
            ciphertext_b64=ciphertext_b64,
            key_id=key_id if key_id else None,
        )
        print(f"Decrypted with key: {response['key_id']}")
        print(f"Algorithm: {response['encryption_algorithm']}")
        print(f"Plaintext (b64): {response['plaintext_b64']}")
        try:
            plaintext = base64.b64decode(response["plaintext_b64"]).decode("utf-8")
            print(f"Plaintext (text): {plaintext}")
        except Exception:
            print("Plaintext is not valid UTF-8 text.")
    else:
        print("Set KMS_CIPHERTEXT_B64 environment variable to run decryption.")
