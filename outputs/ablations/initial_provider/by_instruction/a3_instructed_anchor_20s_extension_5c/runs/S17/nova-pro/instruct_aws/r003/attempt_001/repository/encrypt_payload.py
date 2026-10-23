import boto3
from security_client import get_kms_client

def encrypt_payload(plaintext):
    kms_client = get_kms_client()
    response = kms_client.encrypt(
        KeyId='alias/example_key',
        Plaintext=plaintext
    )
    return response['CiphertextBlob']