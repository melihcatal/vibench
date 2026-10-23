import os
from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse


def decrypt_payload(ciphertext: bytes, key_id: str = None) -> DecryptionResponse:
    client = get_kms_client()
    request = DecryptionRequest(
        ciphertext=ciphertext,
        key_id=key_id
    )
    
    decrypt_kwargs = {"CiphertextBlob": request.ciphertext}
    if request.key_id:
        decrypt_kwargs["KeyId"] = request.key_id
    
    response = client.decrypt(**decrypt_kwargs)
    
    return DecryptionResponse(
        plaintext=response["Plaintext"].decode("utf-8"),
        key_id=response["KeyId"],
        algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT")
    )