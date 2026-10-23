import base64
from security_client import get_kms_client, get_data_key_id

def decrypt_payload(ciphertext_base64: str) -> str:
    """Decrypt ciphertext encrypted with the managed KMS.

    Expects the ciphertext_base64 produced by encrypt_payload.
    """
    client = get_kms_client()
    ciphertext_blob = base64.b64decode(ciphertext_base64)
    key_id = get_data_key_id()  # same key used for decryption
    response = client.decrypt(CiphertextBlob=ciphertext_blob)
    return response['Plaintext'].decode('utf-8')
