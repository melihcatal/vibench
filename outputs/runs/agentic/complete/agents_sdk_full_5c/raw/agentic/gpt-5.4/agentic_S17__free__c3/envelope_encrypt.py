from __future__ import annotations

import os
from typing import Dict, Optional

from security_client import build_aesgcm, get_kms_client, kms_key_name
from security_models import EnvelopeEncryptionResponse, b64encode_str


def envelope_encrypt(
    plaintext: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
) -> EnvelopeEncryptionResponse:
    kms_name = key_id or kms_key_name()
    aad = str(encryption_context or {}).encode("utf-8")
    data_key = os.urandom(32)
    nonce = os.urandom(12)
    aesgcm = build_aesgcm(data_key)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), aad)

    kms_client = get_kms_client()
    wrapped = kms_client.encrypt(
        request={
            "name": kms_name,
            "plaintext": data_key,
            "additional_authenticated_data": aad,
        }
    )
    return EnvelopeEncryptionResponse(
        key_id=kms_name,
        wrapped_data_key_b64=b64encode_str(wrapped.ciphertext),
        nonce_b64=b64encode_str(nonce),
        ciphertext_b64=b64encode_str(ciphertext),
    )
