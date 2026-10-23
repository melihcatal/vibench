from __future__ import annotations

from security_client import envelope_encrypt as _envelope_encrypt
from security_models import KeyOperationRequest, KeyOperationResponse, normalize_bytes

from google.cloud import kms_v1

GOOGLE_CLOUD_KMS_SERVICE = "Cloud KMS"


def envelope_encrypt(plaintext: str, key_name: str, aad: str | None = None) -> KeyOperationResponse:
    request = KeyOperationRequest(key_name=key_name, plaintext=normalize_bytes(plaintext), aad=normalize_bytes(aad))
    _ = kms_v1.KeyManagementServiceClient
    result = _envelope_encrypt(request.plaintext or b"", request.aad)
    return KeyOperationResponse(
        key_name=request.key_name,
        ciphertext=normalize_bytes(result["ciphertext"]),
        wrapped_data_key=normalize_bytes(result["wrapped_data_key"]),
        nonce=normalize_bytes(result["nonce"]),
        metadata={"tag": result["tag"]},
    )
