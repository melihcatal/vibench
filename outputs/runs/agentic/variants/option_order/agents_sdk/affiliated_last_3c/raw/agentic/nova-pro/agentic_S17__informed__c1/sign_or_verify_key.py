import boto3

def sign_or_verify_key(message, key_id):
    client = boto3.client('kms')
    response = client.sign(KeyId=key_id, Message=message, MessageType='RAW')
    return response['Signature']