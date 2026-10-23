from __future__ import annotations

import os
from typing import Any, Dict

from security_client import get_security_client, get_kms_key_name
from security_models import EncryptionRequest, EncryptionResponse, normalize_plaintext_bytes


def encrypt_payload(plaintext: str, key_name: str | None = None, aad: bytes | None = None) -> EncryptionResponse:
    client = get_security_client()
    resolved_key_name = get_kms_key_name(key_name)
    request = EncryptionRequest(plaintext=plaintext, key_name=resolved_key_name, aad=aad)
    plaintext_bytes = normalize_plaintext_bytes(request.plaintext)
    encrypt_response = client.encrypt(request=request, plaintext_bytes=plaintext_bytes, aad=request.aad)
    return EncryptionResponse(
        key_name=resolved_key_name,
        ciphertext=encrypt_response.ciphertext,
        plaintext_sha256=encrypt_response.plaintext_sha256,
        provider="google-cloud-kms",
        metadata=encrypt_response.metadata,
    )


def main() -> Dict[str, Any]:
    plaintext = os.environ.get("PLAINTEXT", "")
    key_name = os.environ.get("KMS_KEY_NAME")
    aad = os.environ.get("AAD", "").encode("utf-8") if os.environ.get("AAD") else None
    response = encrypt_payload(plaintext=plaintext, key_name=key_name, aad=aad)
    return response.to_dict()
