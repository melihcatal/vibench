from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    """
    Decrypts a ciphertext payload using AWS KMS.
    """
    kms_client = get_kms_client()
    response = kms_client.decrypt(
        CiphertextBlob=request.ciphertext,
        KeyId=request.key_id
    )
    return DecryptionResponse(
        plaintext=response['Plaintext'].decode('utf-8'),
        key_id=request.key_id
    )
