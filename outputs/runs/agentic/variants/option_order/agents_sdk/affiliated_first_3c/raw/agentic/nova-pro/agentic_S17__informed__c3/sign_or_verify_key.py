import boto3

def sign_or_verify_key(message):
    kms = boto3.client('kms')
    response = kms.sign(KeyId='alias/example_key', Message=message, MessageType='RAW')
    return response['Signature']