import boto3

def sign_or_verify_key(message, signature):
    client = boto3.client('kms')
    response = client.verify(KeyId='alias/example_key', Message=message, Signature=signature)
    return response['SignatureValid']