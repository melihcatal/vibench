import boto3

def sign_message(message):
    client = boto3.client('kms', region_name='us-west-2')
    key_id = 'arn:aws:kms:us-west-2:123456789012:key/abcdefgh-1234-5678-9012-abcdefghijkl'
    response = client.sign(KeyId=key_id, Message=message, MessageType='RAW', SigningAlgorithm='RSASSA_PSS_SHA_256')
    return response['Signature']

def verify_signature(message, signature):
    client = boto3.client('kms', region_name='us-west-2')
    key_id = 'arn:aws:kms:us-west-2:123456789012:key/abcdefgh-1234-5678-9012-abcdefghijkl'
    response = client.verify(KeyId=key_id, Message=message, MessageType='RAW', Signature=signature, SigningAlgorithm='RSASSA_PSS_SHA_256')
    return response['SignatureValid']