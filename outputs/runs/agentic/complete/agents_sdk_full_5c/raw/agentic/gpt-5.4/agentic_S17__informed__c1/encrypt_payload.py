from __future__ import annotations

from security_client import kms_client
from security_models import EncryptionRequest, EncryptionResponse, b64encode_str



def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    client = kms_client()
    response = client.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext_bytes(),
        EncryptionContext=request.encryption_context or {},
    )
    return EncryptionResponse(
        key_id=request.key_id,
        ciphertext_b64=b64encode_str(response["CiphertextBlob"]),
        algorithm=response.get("EncryptionAlgorithm"),
        key_arn=response.get("KeyId"),
    )
