from __future__ import annotations

import os
from typing import Any, Dict

from security_client import get_security_client, get_kms_key_name
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse


def envelope_encrypt(plaintext: str, key_name: str | None = None, aad: bytes | None = None) -> EnvelopeEncryptionResponse:
    client = get_security_client()
    resolved_key_name = get_kms_key_name(key_name)
    request = EnvelopeEncryptionRequest(plaintext=plaintext, key_name=resolved_key_name, aad=aad)
    response = client.envelope_encrypt(request=request)
    return EnvelopeEncryptionResponse(
        key_name=resolved_key_name,
        encrypted_data_key=response.encrypted_data_key,
        iv=response.iv,
        ciphertext=response.ciphertext,
        provider="google-cloud-kms",
        metadata=response.metadata,
    )


def main() -> Dict[str, Any]:
    plaintext = os.environ.get("PLAINTEXT", "")
    key_name = os.environ.get("KMS_KEY_NAME")
    aad = os.environ.get("AAD", "").encode("utf-8") if os.environ.get("AAD") else None
    response = envelope_encrypt(plaintext=plaintext, key_name=key_name, aad=aad)
    return response.to_dict()
