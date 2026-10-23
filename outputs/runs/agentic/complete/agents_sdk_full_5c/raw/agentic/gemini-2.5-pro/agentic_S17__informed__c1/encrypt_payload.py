# encrypt_payload.py
from security_client import get_aws_kms_client
from security_models import EncryptionPayload

def encrypt_with_kms(payload: EncryptionPayload) -> bytes:
    """
    Encrypts a plaintext payload using AWS KMS.
    """
    kms_client = get_aws_kms_client()
    
    response = kms_client.encrypt(
        KeyId=payload.key_id,
        Plaintext=payload.plaintext
    )
    return response['CiphertextBlob']
