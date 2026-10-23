"""
encrypt_payload.py - Encrypts a plaintext payload with a managed key using AWS KMS.

Provider: AWS Key Management Service (KMS)
Service endpoint: kms.{region}.amazonaws.com
Concrete model: AWS KMS symmetric encryption (SYMMETRIC_DEFAULT)
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
    EncryptRequest,
    EncryptResponse,
    encode_bytes,
    normalize_key_id,
    build_encryption_context,
)


def encrypt_payload(
    plaintext: str,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
    grant_tokens: Optional[List[str]] = None,
    config: Optional[SecurityClientConfig] = None,
) -> EncryptResponse:
    """
    Encrypt a plaintext payload using AWS KMS managed key.

    Uses the AWS KMS Encrypt API with SYMMETRIC_DEFAULT algorithm.
    AWS KMS supports RSAES_OAEP_SHA_256 for asymmetric keys and
    SYMMETRIC_DEFAULT for symmetric CMKs.

    Args:
        plaintext: The text to encrypt.
        key_id: KMS key ID, key ARN, or alias.
        encryption_context: Optional encryption context dict.
        grant_tokens: Optional grant tokens.
        config: Optional SecurityClientConfig.

    Returns:
        EncryptResponse with base64-encoded ciphertext.
    """
    kms_client = create_kms_client(config)
    normalized_key_id = normalize_key_id(key_id)

    plaintext_bytes = plaintext.encode("utf-8")

    encrypt_kwargs = {
        "KeyId": normalized_key_id,
        "Plaintext": plaintext_bytes,
        "EncryptionAlgorithm": "SYMMETRIC_DEFAULT",
    }

    if encryption_context:
        encrypt_kwargs["EncryptionContext"] = encryption_context

    if grant_tokens:
        encrypt_kwargs["GrantTokens"] = grant_tokens

    try:
        response = kms_client.encrypt(**encrypt_kwargs)
    except Exception as e:
        handle_kms_error(e, context="encrypt_payload")

    ciphertext_blob = encode_bytes(response["CiphertextBlob"])
    response_key_id = extract_key_arn_from_response(response, normalized_key_id)

    return EncryptResponse(
        ciphertext_blob=ciphertext_blob,
        key_id=response_key_id,
        encryption_algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
        ciphertext_type=response.get("CiphertextBlob").__class__.__name__,
    )


def encrypt_payload_from_request(
    request: EncryptRequest,
    config: Optional[SecurityClientConfig] = None,
) -> EncryptResponse:
    """Encrypt payload from a normalized EncryptRequest."""
    return encrypt_payload(
        plaintext=request.plaintext,
        key_id=request.key_id,
        encryption_context=request.encryption_context,
        grant_tokens=request.grant_tokens,
        config=config,
    )


if __name__ == "__main__":
    key_id = os.environ.get("KMS_KEY_ID", "alias/default")
    plaintext = os.environ.get("PLAINTEXT", "sensitive-data-to-encrypt")
    encryption_context = build_encryption_context(
        purpose="demo",
        environment=os.environ.get("ENVIRONMENT", "development"),
    )
    response = encrypt_payload(plaintext, key_id, encryption_context)
    print(f"Key ID: {response.key_id}")
    print(f"Algorithm: {response.encryption_algorithm}")
    print(f"Ciphertext (first 64 chars): {response.ciphertext_blob[:64]}...")
