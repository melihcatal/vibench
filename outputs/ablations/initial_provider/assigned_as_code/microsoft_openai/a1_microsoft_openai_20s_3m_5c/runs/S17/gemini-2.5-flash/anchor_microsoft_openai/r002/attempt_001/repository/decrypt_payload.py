from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(request: DecryptionRequest, config=None) -> DecryptionResponse:
    config = config or {}
    with DefaultAzureCredential() as credential:
        with CryptographyClient(request.key_id, credential=credential) as client:
            response = client.decrypt(request.algorithm, request.ciphertext, iv=request.iv, authentication_tag=request.tag)
    return DecryptionResponse(plaintext=response.plaintext, key_id=response.key_id, algorithm=request.algorithm)
