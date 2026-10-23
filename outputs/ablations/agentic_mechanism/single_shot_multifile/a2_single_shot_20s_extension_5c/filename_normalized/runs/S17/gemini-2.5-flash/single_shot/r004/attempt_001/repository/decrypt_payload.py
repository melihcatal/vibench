import base64
from security_client import SecurityClientConfig
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    kms_client = SecurityClientConfig.get_kms_client()

    response = kms_client.decrypt(
        CiphertextBlob=request.ciphertext_blob
    )

    return DecryptionResponse(
        plaintext=response["Plaintext"]
    )