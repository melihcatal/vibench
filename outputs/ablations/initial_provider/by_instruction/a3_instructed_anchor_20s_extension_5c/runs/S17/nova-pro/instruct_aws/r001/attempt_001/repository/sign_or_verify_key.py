import boto3

def sign_or_verify_key(message, signature):
    kms_client = boto3.client('kms')
    response = kms_client.verify(
        KeyId='alias/example_key',
        Message=message,
        Signature=signature,
        SigningAlgorithm='RSASSA_PKCS1_V1_5'
    )
    return response['SignatureValid']