import boto3
import os

# Initialize a session using Amazon KMS
session = boto3.Session()
kms = session.client('kms')

# Local configuration for KMS
def get_kms_config():
    return {
        'region': os.getenv('AWS_REGION', 'us-west-2'),
        'access_key': os.getenv('AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('AWS_SECRET_ACCESS_KEY')
    }

# Helper utility to encrypt data
def encrypt_data(plaintext):
    response = kms.encrypt(
        KeyId=os.getenv('KMS_KEY_ID'),
        Plaintext=plaintext
    )
    return response['CiphertextBlob']

# Helper utility to decrypt data
def decrypt_data(ciphertext):
    response = kms.decrypt(
        CiphertextBlob=ciphertext
    )
    return response['Plaintext']