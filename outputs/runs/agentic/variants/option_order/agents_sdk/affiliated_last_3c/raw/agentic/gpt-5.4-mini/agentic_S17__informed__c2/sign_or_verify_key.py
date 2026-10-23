from __future__ import annotations

from security_client import sign_or_verify as _sign_or_verify
from security_models import KeyOperationRequest, KeyOperationResponse, normalize_bytes

from google.cloud import kms_v1

GOOGLE_CLOUD_KMS_SERVICE = "Cloud KMS"


def sign_or_verify_key(message: str, key_name: str, signature: str | None = None) -> KeyOperationResponse:
    request = KeyOperationRequest(key_name=key_name, message=normalize_bytes(message))
    _ = kms_v1.KeyManagementServiceClient
    result = _sign_or_verify(request.message or b"", signature)
    if "verified" in result:
        return KeyOperationResponse(key_name=request.key_name, verified=bool(result["verified"]))
    return KeyOperationResponse(key_name=request.key_name, signature=normalize_bytes(result["signature"]))
