import boto3
from cryptography.fernet import Fernet

def envelope_encrypt(plaintext):
    kms_client = boto3.client('kms', region_name='us-west-2')
    key_id = 'arn:aws:kms:us-west-2:123456789012:key/abcdefgh-1234-5678-9012-abcdefghijkl'
    data_key = Fernet.generate_key()
    encrypted_data_key = kms_client.encrypt(KeyId=key_id, Plaintext=data_key)
    fernet = Fernet(data_key)
    encrypted_text = fernet.encrypt(plaintext.encode())
    return encrypted_text, encrypted_data_key['CiphertextBlob']