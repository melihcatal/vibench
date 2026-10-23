from __future__ import annotations

import os
from typing import Any, Dict, Optional

from google.cloud import kms_v1

from security_client import build_kms_client, resolve_crypto_key_name
from security_models import DecryptRequest, DecryptResponse, from_json_safe_bytes, to_json_safe_bytes


def decrypt_payload(ciphertext: str, key_name: Optional[str] = None, aad: Optional[bytes] = None) -> Dict[str, Any]:
    client = build_kms_client()
    crypto_key = resolve_crypto_key_name(key_name or os.getenv("GOOGLE_CLOUD_KMS_CRYPTO_KEY"))
    request = DecryptRequest(ciphertext=from_json_safe_bytes(ciphertext), key_name=crypto_key, aad=aad)
    response = client.decrypt(
        request={
            "name": request.key_name,
            "ciphertext": request.ciphertext,
            "additional_authenticated_data": request.aad or b"",
        }
    )
    result = DecryptResponse(
        key_name=crypto_key,
        plaintext=response.plaintext,
        aad=request.aad,
    )
    return {
        "key_name": result.key_name,
        "plaintext": to_json_safe_bytes(result.plaintext),
        "aad": to_json_safe_bytes(result.aad),
    }
