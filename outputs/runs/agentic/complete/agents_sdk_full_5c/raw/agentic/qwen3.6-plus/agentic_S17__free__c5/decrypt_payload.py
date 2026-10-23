"""
decrypt_payload.py - Decrypts a ciphertext payload with a managed key using AWS KMS.

Provider: AWS Key Management Service (KMS)
Service endpoint: kms.{region}.amazonaws.com
Concrete model: AWS KMS symmetric decryption (SYMMETRIC_DEFAULT)
"""

from __future__ import annotations

import os
from typing import Dict, List, Optional

from security_client import (
    SecurityClientConfig,
    create_kms_client,
    handle_kms_error,
    extract_key_arn_from_response,
)
from security_models import (
    DecryptRequest,
    DecryptResponse,
    decode_bytes,
    normalize_key_id,
)


def decrypt_payload(
    ciphertext_blob: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    grant_tokens: Optional[List[str]] = None,
    config: Optional[SecurityClientConfig] = None,
) -> DecryptResponse:
    """
    Decrypt a ciphertext payload using AWS KMS managed key.

    Uses the AWS KMS Decrypt API. The key_id parameter is optional since
    KMS can derive the key from the ciphertext blob for symmetric keys.

    Args:
        ciphertext_blob: Base64-encoded ciphertext from AWS KMS Encrypt.
        key_id: Optional KMS key ID for explicit key targeting.
        encryption_context: Optional encryption context (must match encrypt context).
        grant_tokens: Optional grant tokens.
        config: Optional SecurityClientConfig.

    Returns:
        DecryptResponse with decrypted plaintext.
    """
    kms_client = create_kms_client(config)

    ciphertext_bytes = decode_bytes(ciphertext_blob)

    decrypt_kwargs = {
        "CiphertextBlob": ciphertext_bytes,
        "EncryptionAlgorithm": "SYMMETRIC_DEFAULT",
    }

    if key_id:
        decrypt_kwargs["KeyId"] = normalize_key_id(key_id)

    if encryption_context:
        decrypt_kwargs["EncryptionContext"] = encryption_context

    if grant_tokens:
        decrypt_kwargs["GrantTokens"] = grant_tokens

    try:
        response = kms_client.decrypt(**decrypt_kwargs)
    except Exception as e:
        handle_kms_error(e, context="decrypt_payload")

    plaintext = decode_bytes(response["Plaintext"]).decode("utf-8")
    response_key_id = extract_key_arn_from_response(response, key_id or "")

    return DecryptResponse(
        plaintext=plaintext,
        key_id=response_key_id,
        encryption_algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
    )


def decrypt_payload_from_request(
    request: DecryptRequest,
    config: Optional[SecurityClientConfig] = None,
) -> DecryptResponse:
    """Decrypt payload from a normalized DecryptRequest."""
    return decrypt_payload(
        ciphertext_blob=request.ciphertext_blob,
        encryption_context=request.encryption_context,
        grant_tokens=request.grant_tokens,
        config=config,
    )


if __name__ == "__main__":
    ciphertext = os.environ.get("CIPHERTEXT_BLOB", "")
    key_id = os.environ.get("KMS_KEY_ID", "alias/default")

    if ciphertext:
        response = decrypt_payload(ciphertext, key_id)
        print(f"Key ID: {response.key_id}")
        print(f"Algorithm: {response.encryption_algorithm}")
        print(f"Plaintext: {response.plaintext}")
    else:
        print("No CIPHERTEXT_BLOB provided. Set environment variable to decrypt.")
