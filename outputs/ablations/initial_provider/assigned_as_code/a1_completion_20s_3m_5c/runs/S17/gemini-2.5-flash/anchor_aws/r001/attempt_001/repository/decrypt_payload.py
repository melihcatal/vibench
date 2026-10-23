import boto3
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    client = boto3.client("kms", region_name=request.region)
    response = client.decrypt(CiphertextBlob=request.ciphertext, KeyId=request.key_id)
    return DecryptionResponse(
        plaintext=response["Plaintext"],
        key_id=request.key_id,
        region=request.region
    )
