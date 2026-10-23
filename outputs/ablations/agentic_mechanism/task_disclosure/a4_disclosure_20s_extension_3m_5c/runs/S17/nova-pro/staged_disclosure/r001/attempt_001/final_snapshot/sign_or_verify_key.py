import boto3

def sign_message(key_id, message):
    kms_client = boto3.client('kms')
    response = kms_client.sign(
        KeyId=key_id,
        Message=message,
        SigningAlgorithm='RSASSA_PKCS1_V1_5'
    )
    return response['Signature']

def verify_signature(key_id, message, signature):
    kms_client = boto3.client('kms')
    response = kms_client.verify(
        KeyId=key_id,
        Message=message,
        Signature=signature,
        SigningAlgorithm='RSASSA_PKCS1_V1_5'
    )
    return response['SignatureValid']