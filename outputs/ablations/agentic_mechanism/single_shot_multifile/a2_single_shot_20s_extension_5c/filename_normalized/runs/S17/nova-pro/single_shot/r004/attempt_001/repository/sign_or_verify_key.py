import boto3

from security_client import get_kms_client

def sign_or_verify_key(message, signature):
    kms_client = get_kms_client()
    key_id = 'arn:aws:kms:us-west-2:123456789012:key/abcd1234-abcd-1234-abcd-abcd1234abcd'
    response = kms_client.verify(KeyId=key_id, Message=message, Signature=signature, SigningAlgorithm='RSASSA_PSS_SHA_256')
    return response['SignatureValid']