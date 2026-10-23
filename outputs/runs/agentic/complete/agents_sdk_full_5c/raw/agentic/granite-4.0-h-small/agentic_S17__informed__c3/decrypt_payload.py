import os
import boto3
from security_client import get_kms_client

kms_client = get_kms_client()

def decrypt_payload(ciphertext_blob: bytes) -> str:
    """Decrypt a ciphertext blob using AWS KMS and return the plaintext (utf-8 string)."""
    response = kms_client.decrypt(
        CiphertextBlob=ciphertext_blob
    )
    return response['Plaintext'].decode('utf-8')

if __name__ == "__main__":
    test_key_id = os.getenv('AWS_KMS_KEY_ID')
    if not test_key_id:
        raise RuntimeError('Set AWS_KMS_KEY_ID environment variable')
    # Reuse encrypt_payload.py sample for demonstration
    import encrypt_payload
    ct = encrypt_payload.encrypt_payload('Hello, decryption!', test_key_id)
    pt = decrypt_payload(ct)
    print('Decrypted text:', pt)
