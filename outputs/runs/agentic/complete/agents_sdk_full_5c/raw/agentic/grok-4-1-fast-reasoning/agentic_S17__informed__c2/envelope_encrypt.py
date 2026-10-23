import boto3
import base64
import os
from cryptography.fernet import Fernet

def envelope_encrypt(plaintext: str, key_id: str = os.getenv('KMS_KEY_ID')) -> tuple[str, str]:
    """
    Implements envelope encryption: DEK encrypts data, KMS encrypts DEK.
    Returns (encrypted_dek_b64, data_ciphertext_b64)
    """
    dek = Fernet.generate_key()
    fernet = Fernet(dek)
    data_ciphertext = fernet.encrypt(plaintext.encode('utf-8'))
    client = boto3.client('kms')
    response = client.encrypt(
        KeyId=key_id,
        Plaintext=dek
    )
    encrypted_dek = response['CiphertextBlob']
    return (
        base64.b64encode(encrypted_dek).decode('utf-8'),
        base64.b64encode(data_ciphertext).decode('utf-8')
    )