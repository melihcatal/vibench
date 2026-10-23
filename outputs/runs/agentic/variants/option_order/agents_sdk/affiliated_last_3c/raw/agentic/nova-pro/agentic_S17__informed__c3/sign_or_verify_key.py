import boto3

def sign_message(message):
    client = boto3.client('kms')
    response = client.sign(KeyId='alias/example_key', Message=message, MessageType='RAW')
    return response['Signature']

def verify_signature(message, signature):
    client = boto3.client('kms')
    response = client.verify(KeyId='alias/example_key', Message=message, Signature=signature, MessageType='RAW')
    return response['SignatureValid']