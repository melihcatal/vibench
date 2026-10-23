from __future__ import annotations

from security_client import kms_client
from security_models import DecryptionRequest, DecryptionResponse



def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    client = kms_client()
    response = client.decrypt(
        CiphertextBlob=request.ciphertext_bytes(),
        EncryptionContext=request.encryption_context or {},
    )
    return DecryptionResponse(
        plaintext=response["Plaintext"].decode("utf-8"),
        key_id=response.get("KeyId"),
        encryption_algorithm=response.get("EncryptionAlgorithm"),
    )
