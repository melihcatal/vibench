import boto3
from cryptography.fernet import Fernet

from security_client import get_kms_client

def envelope_encrypt(data):
    kms_client = get_kms_client()
    key_id = 'arn:aws:kms:us-west-2:123456789012:key/abcd1234-abcd-1234-abcd-abcd1234abcd'
    data_key = Fernet.generate_key()
    encrypted_data_key = kms_client.encrypt(KeyId=key_id, Plaintext=data_key)
    fernet = Fernet(data_key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data, encrypted_data_key['CiphertextBlob']