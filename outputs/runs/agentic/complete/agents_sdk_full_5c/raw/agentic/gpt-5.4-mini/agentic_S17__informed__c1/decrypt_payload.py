from __future__ import annotations

from security_client import SecurityClient
from security_models import KeyOperationRequest, KeyOperationResponse


AWS_KMS_PROVIDER = "boto3:kms"


def decrypt_payload(request: KeyOperationRequest) -> KeyOperationResponse:
    client = SecurityClient()
    plaintext = client.decrypt(
        ciphertext_b64=request.ciphertext_b64 or "",
        aad=request.additional_authenticated_data,
    )
    return KeyOperationResponse(key_id=request.key_id, result=plaintext, metadata={"provider": AWS_KMS_PROVIDER})
