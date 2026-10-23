from __future__ import annotations

from security_client import decrypt_payload as _decrypt_payload
from security_models import KeyOperationRequest, KeyOperationResponse, normalize_bytes

from google.cloud import kms_v1

GOOGLE_CLOUD_KMS_SERVICE = "Cloud KMS"


def decrypt_payload(ciphertext: str, key_name: str) -> KeyOperationResponse:
    request = KeyOperationRequest(key_name=key_name, ciphertext=normalize_bytes(ciphertext))
    _ = kms_v1.KeyManagementServiceClient
    plaintext = _decrypt_payload(ciphertext)
    return KeyOperationResponse(key_name=request.key_name, plaintext=normalize_bytes(plaintext))
