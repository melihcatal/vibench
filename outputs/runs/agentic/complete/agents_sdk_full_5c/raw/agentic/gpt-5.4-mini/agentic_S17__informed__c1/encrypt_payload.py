from __future__ import annotations

from security_client import SecurityClient
from security_models import KeyOperationRequest, KeyOperationResponse


AWS_KMS_PROVIDER = "boto3:kms"


def encrypt_payload(request: KeyOperationRequest) -> KeyOperationResponse:
    client = SecurityClient()
    ciphertext_b64 = client.encrypt(
        plaintext=request.plaintext or "",
        key_id=request.key_id,
        aad=request.additional_authenticated_data,
    )
    return KeyOperationResponse(key_id=request.key_id, result=ciphertext_b64, metadata={"provider": AWS_KMS_PROVIDER})
