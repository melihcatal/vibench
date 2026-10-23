from security_client import SecurityClient
from security_models import EncryptionRequest, EncryptionResponse

def encrypt_payload(payload: EncryptionRequest) -> EncryptionResponse:
    """Encrypts a plaintext payload with a managed key from AWS KMS."""
    kms_client = SecurityClient.get_kms_client()

    response = kms_client.encrypt(
        KeyId=payload.key_id,
        Plaintext=payload.plaintext
    )

    ciphertext_blob = response['CiphertextBlob']
    
    return EncryptionResponse(
        ciphertext=ciphertext_blob,
        key_id=payload.key_id
    )
