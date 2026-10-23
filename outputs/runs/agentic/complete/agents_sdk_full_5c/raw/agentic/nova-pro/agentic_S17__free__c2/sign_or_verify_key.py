import boto3

def sign_or_verify_key(message):
    client = boto3.client('kms')
    sign = client.sign(KeyId='alias/example_key', Message=message, MessageType='RAW')
    return sign['Signature']