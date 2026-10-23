import boto3

def sign_message(key_id, message):
    kms_client = boto3.client('kms')
    response = kms_client.sign(KeyId=key_id, Message=message, MessageType='RAW')
    return response['Signature']

def verify_signature(key_id, message, signature):
    kms_client = boto3.client('kms')
    response = kms_client.verify(KeyId=key_id, Message=message, Signature=signature, MessageType='RAW')
    return response['SignatureValid']