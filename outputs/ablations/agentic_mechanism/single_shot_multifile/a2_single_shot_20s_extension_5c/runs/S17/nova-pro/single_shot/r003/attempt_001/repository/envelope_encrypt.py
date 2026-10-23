from security_client import get_kms_client
import base64
from cryptography.fernet import Fernet

def envelope_encrypt(data):
    client = get_kms_client()
    data_key = Fernet.generate_key()
    cipher_suite = Fernet(data_key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    encrypted_data_key = client.encrypt(KeyId='alias/myKey', Plaintext=data_key)
    return base64.b64encode(encrypted_data).decode(), encrypted_data_key['CiphertextBlob']