import base64
from botocore.exceptions import ClientError
from security_client import kms_client
from security_models import EncryptionRequest, EncryptionResponse

def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    """
    Encrypts a plaintext payload using a specified AWS KMS key.
    """
    try:
        client = kms_client.get_client()
        response = client.encrypt(
            KeyId=request.key_id,
            Plaintext=request.plaintext
        )
        ciphertext_blob = response['CiphertextBlob']
        return EncryptionResponse(
            ciphertext=ciphertext_blob,
            key_id=response['KeyId'],
            success=True
        )
    except ClientError as e:
        return EncryptionResponse(
            ciphertext=b'',
            key_id=request.key_id,
            success=False,
            error=str(e)
        )
