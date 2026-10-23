import boto3

def sign_or_verify_key(message):
    kms_client = boto3.client('kms')
    response = kms_client.sign(KeyId='alias/myKey', Message=message, MessageType='RAW')
    return response['Signature']