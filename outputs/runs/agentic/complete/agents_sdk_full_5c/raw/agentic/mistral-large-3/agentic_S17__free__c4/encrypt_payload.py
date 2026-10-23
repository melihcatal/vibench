import os
from security_client import get_kms_client
from security_models import EncryptionRequest, EncryptionResponse


def encrypt_payload(plaintext: str, key_id: str) -> EncryptionResponse:
    client = get_kms_client()
    request = EncryptionRequest(
        key_id=key_id,
        plaintext=plaintext.encode("utf-8")
    )
    
    response = client.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext
    )
    
    return EncryptionResponse(
        ciphertext=response["CiphertextBlob"],
        key_id=response["KeyId"],
        algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT")
    )