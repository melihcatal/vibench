from __future__ import annotations

from security_client import encrypt_payload as _encrypt_payload
from security_models import KeyOperationRequest, KeyOperationResponse, normalize_bytes

from google.cloud import kms_v1

GOOGLE_CLOUD_KMS_SERVICE = "Cloud KMS"


def encrypt_payload(plaintext: str, key_name: str) -> KeyOperationResponse:
    request = KeyOperationRequest(key_name=key_name, plaintext=normalize_bytes(plaintext))
    _ = kms_v1.KeyManagementServiceClient
    ciphertext = _encrypt_payload(request.plaintext or b"")
    return KeyOperationResponse(key_name=request.key_name, ciphertext=normalize_bytes(ciphertext))
