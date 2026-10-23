import boto3

def sign_message(key_id, message):
    kms = boto3.client('kms')
    response = kms.sign(
        KeyId=key_id,
        Message=message,
        SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256'
    )
    return response['Signature']

def verify_signature(key_id, message, signature):
    kms = boto3.client('kms')
    response = kms.verify(
        KeyId=key_id,
        Message=message,
        Signature=signature,
        SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256'
    )
    return response['SignatureValid']