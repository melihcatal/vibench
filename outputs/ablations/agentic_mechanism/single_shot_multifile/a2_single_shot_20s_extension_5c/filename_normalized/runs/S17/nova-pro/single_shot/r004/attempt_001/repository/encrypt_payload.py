import boto3

from security_client import get_kms_client

def encrypt_payload(plaintext):
    kms_client = get_kms_client()
    key_id = 'arn:aws:kms:us-west-2:123456789012:key/abcd1234-abcd-1234-abcd-abcd1234abcd'
    response = kms_client.encrypt(KeyId=key_id, Plaintext=plaintext)
    return response['CiphertextBlob']