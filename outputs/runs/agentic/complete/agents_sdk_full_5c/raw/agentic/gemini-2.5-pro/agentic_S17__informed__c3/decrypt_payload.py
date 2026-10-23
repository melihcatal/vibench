from security_client import SecurityClient
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(payload: DecryptionRequest) -> DecryptionResponse:
    """Decrypts a ciphertext payload with a managed key from AWS KMS."""
    kms_client = SecurityClient.get_kms_client()

    response = kms_client.decrypt(
        KeyId=payload.key_id,
        CiphertextBlob=payload.ciphertext
    )

    plaintext = response['Plaintext']
    
    return DecryptionResponse(
        plaintext=plaintext,
        key_id=payload.key_id
    )
