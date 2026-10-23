import boto3

def sign_or_verify_key(message):
    client = boto3.client('kms')
    response = client.sign(KeyId='alias/example-key', Message=message, MessageType='RAW')
    return response['Signature']