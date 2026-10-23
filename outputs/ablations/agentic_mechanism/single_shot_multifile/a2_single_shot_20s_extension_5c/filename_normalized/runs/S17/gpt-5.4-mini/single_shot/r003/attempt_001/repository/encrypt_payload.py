from __future__ import annotations

import os
from typing import Any, Dict, Optional

from google.cloud import kms_v1
from google.protobuf.field_mask_pb2 import FieldMask

from security_client import build_kms_client, resolve_crypto_key_name
from security_models import EncryptRequest, EncryptResponse, normalize_plaintext_bytes, to_json_safe_bytes


def encrypt_payload(plaintext: str, key_name: Optional[str] = None, aad: Optional[bytes] = None) -> Dict[str, Any]:
    client = build_kms_client()
    crypto_key = resolve_crypto_key_name(key_name or os.getenv("GOOGLE_CLOUD_KMS_CRYPTO_KEY"))
    request = EncryptRequest(plaintext=plaintext, key_name=crypto_key, aad=aad)
    response = client.encrypt(
        request={
            "name": request.key_name,
            "plaintext": normalize_plaintext_bytes(request.plaintext),
            "additional_authenticated_data": request.aad or b"",
        }
    )
    result = EncryptResponse(
        key_name=crypto_key,
        ciphertext=response.ciphertext,
        plaintext_bytes=len(normalize_plaintext_bytes(plaintext)),
        aad=request.aad,
    )
    return {
        "key_name": result.key_name,
        "ciphertext": to_json_safe_bytes(result.ciphertext),
        "plaintext_bytes": result.plaintext_bytes,
        "aad": to_json_safe_bytes(result.aad),
    }
