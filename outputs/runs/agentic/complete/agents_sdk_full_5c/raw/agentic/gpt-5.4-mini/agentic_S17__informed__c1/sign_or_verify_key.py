from __future__ import annotations

from security_client import SecurityClient
from security_models import KeyOperationRequest, KeyOperationResponse


AWS_KMS_PROVIDER = "boto3:kms"


def sign_or_verify_key(request: KeyOperationRequest, verify_only: bool = False) -> KeyOperationResponse:
    client = SecurityClient()
    if verify_only:
        valid = client.verify(
            message=request.plaintext or "",
            signature_b64=request.ciphertext_b64 or "",
            signing_key_id=request.key_id,
        )
        return KeyOperationResponse(key_id=request.key_id, result=str(valid), metadata={"provider": AWS_KMS_PROVIDER})

    signature_b64 = client.sign(message=request.plaintext or "", signing_key_id=request.key_id)
    return KeyOperationResponse(key_id=request.key_id, result=signature_b64, metadata={"provider": AWS_KMS_PROVIDER})
