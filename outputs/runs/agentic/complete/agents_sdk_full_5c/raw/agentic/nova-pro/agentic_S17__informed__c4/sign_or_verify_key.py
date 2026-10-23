import boto3

def sign_or_verify_key(message, signature):
    kms = boto3.client('kms')
    response = kms.verify(KeyId='alias/myKey', Message=message, Signature=signature)
    return response['SignatureValid']