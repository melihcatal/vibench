from botocore.exceptions import ClientError
from security_client import kms_client
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    """
    Decrypts a ciphertext payload using AWS KMS.
    """
    try:
        client = kms_client.get_client()
        response = client.decrypt(
            CiphertextBlob=request.ciphertext
        )
        plaintext = response['Plaintext']
        return DecryptionResponse(
            plaintext=plaintext,
            key_id=response['KeyId'],
            success=True
        )
    except ClientError as e:
        return DecryptionResponse(
            plaintext=b'',
            key_id="",
            success=False,
            error=str(e)
        )
