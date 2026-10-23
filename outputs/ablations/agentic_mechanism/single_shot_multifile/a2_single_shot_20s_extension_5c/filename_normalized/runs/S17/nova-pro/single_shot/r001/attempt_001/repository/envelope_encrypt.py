from security_client import kms_client
import base64
from cryptography.fernet import Fernet

def envelope_encrypt(data):
    response = kms_client.generate_data_key(KeyId='alias/myKey', KeySpec='AES_256')
    plaintext_data_key = response['Plaintext']
    fernet = Fernet(base64.urlsafe_b64encode(plaintext_data_key))
    encrypted_data = fernet.encrypt(data.encode())
    return {'encrypted_data': encrypted_data, 'encrypted_data_key': response['CiphertextBlob']}