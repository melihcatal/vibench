import boto3

from security_client import get_kms_client

def decrypt_payload(ciphertext):
    kms_client = get_kms_client()
    response = kms_client.decrypt(CiphertextBlob=ciphertext)
    return response['Plaintext']