import boto3

def sign_or_verify_key(message):
    client = boto3.client('kms')
    response = client.sign(KeyId='alias/myKey', Message=message, MessageType='RAW', SigningAlgorithm='RSASSA_PSS_SHA_256')
    return response['Signature']