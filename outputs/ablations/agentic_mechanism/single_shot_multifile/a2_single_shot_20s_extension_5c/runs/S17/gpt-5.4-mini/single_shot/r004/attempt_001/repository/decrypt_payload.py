from __future__ import annotations

import os
from typing import Any, Dict

from security_client import get_security_client, get_kms_key_name
from security_models import DecryptionRequest, DecryptionResponse, normalize_ciphertext_bytes


def decrypt_payload(ciphertext: str, key_name: str | None = None, aad: bytes | None = None) -> DecryptionResponse:
    client = get_security_client()
    resolved_key_name = get_kms_key_name(key_name)
    request = DecryptionRequest(ciphertext=ciphertext, key_name=resolved_key_name, aad=aad)
    ciphertext_bytes = normalize_ciphertext_bytes(request.ciphertext)
    decrypt_response = client.decrypt(request=request, ciphertext_bytes=ciphertext_bytes, aad=request.aad)
    return DecryptionResponse(
        key_name=resolved_key_name,
        plaintext=decrypt_response.plaintext,
        provider="google-cloud-kms",
        metadata=decrypt_response.metadata,
    )


def main() -> Dict[str, Any]:
    ciphertext = os.environ.get("CIPHERTEXT", "")
    key_name = os.environ.get("KMS_KEY_NAME")
    aad = os.environ.get("AAD", "").encode("utf-8") if os.environ.get("AAD") else None
    response = decrypt_payload(ciphertext=ciphertext, key_name=key_name, aad=aad)
    return response.to_dict()
