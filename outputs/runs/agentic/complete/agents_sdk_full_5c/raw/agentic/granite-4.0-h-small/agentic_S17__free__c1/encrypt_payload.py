import base64
from security_client import get_kms_client, get_encryption_key_id

def encrypt_payload(plaintext: str) -> dict:
    """Encrypt plaintext using a managed KMS.

    Returns a dict with ciphertext_base64 and additional metadata.
    """
    client = get_kms_client()
    key_id = get_encryption_key_id()
    # Example using AWS KMS SDK
    response = client.encrypt(KeyId=key_id, Plaintext=plaintext.encode('utf-8'))
    ciphertext = base64.b64encode(response['CiphertextBlob']).decode('utf-8')
    return {
        'ciphertext_base64': ciphertext,
        'key_id': key_id,
        'encryption_context': response.get('EncryptionContext')
    }
