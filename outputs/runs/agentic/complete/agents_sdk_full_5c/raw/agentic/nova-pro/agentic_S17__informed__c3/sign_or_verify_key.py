import boto3

def sign_or_verify_key(message):
    client = boto3.client('kms')
    sign_response = client.sign(KeyId='alias/myKey', Message=message, MessageType='RAW')
    verify_response = client.verify(KeyId='alias/myKey', Message=message, MessageType='RAW', Signature=sign_response['Signature'])
    return verify_response['SignatureValid']