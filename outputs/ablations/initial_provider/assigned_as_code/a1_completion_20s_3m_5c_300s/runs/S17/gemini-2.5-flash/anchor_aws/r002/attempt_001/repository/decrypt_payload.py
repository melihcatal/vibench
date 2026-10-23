import boto3
from security_client import SecurityClient
from security_models import DecryptionRequest, DecryptionResponse


def decrypt_payload(request: DecryptionRequest, config=None) -> DecryptionResponse:
    config = config or {}
    client = SecurityClient(region_name=config.get("region"))
    response = client.decrypt(
        ciphertext=request.ciphertext,
        encryption_context=request.encryption_context
    )
    return DecryptionResponse(
        plaintext=response["Plaintext"],
        key_id=response["KeyId"],
        encryption_context=request.encryption_context
    )
