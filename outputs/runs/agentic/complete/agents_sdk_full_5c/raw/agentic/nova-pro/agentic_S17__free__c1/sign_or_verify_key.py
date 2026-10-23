import boto3

kms = boto3.client('kms')

def sign_message(message):
    response = kms.sign(
        KeyId='alias/myKey',
        Message=message,
        MessageType='RAW'
    )
    return response['Signature']

def verify_signature(message, signature):
    response = kms.verify(
        KeyId='alias/myKey',
        Message=message,
        MessageType='RAW',
        Signature=signature
    )
    return response['SignatureValid']