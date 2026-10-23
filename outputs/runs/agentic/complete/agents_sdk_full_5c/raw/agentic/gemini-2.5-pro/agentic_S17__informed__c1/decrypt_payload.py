# decrypt_payload.py
from security_client import get_aws_kms_client
from security_models import DecryptionPayload

def decrypt_with_kms(payload: DecryptionPayload) -> bytes:
    """
    Decrypts a ciphertext payload using AWS KMS.
    """
    kms_client = get_aws_kms_client()

    try:
        response = kms_client.decrypt(
            KeyId=payload.key_id, 
            CiphertextBlob=payload.ciphertext
        )
        return response['Plaintext']
    except kms_client.exceptions.InvalidCiphertextException as e:
        print(f"Decryption failed: {e}")
        raise
