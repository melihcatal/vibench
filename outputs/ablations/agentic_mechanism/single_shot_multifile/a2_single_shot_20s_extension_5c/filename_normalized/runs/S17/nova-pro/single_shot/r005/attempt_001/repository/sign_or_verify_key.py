import boto3

def sign_or_verify_key(message, signature):
    client = boto3.client('kms', region_name='us-west-2')
    key_id = 'arn:aws:kms:us-west-2:123456789012:key/abcdefgh-1234-5678-9012-abcdefghijkl'
    response = client.verify(KeyId=key_id, Message=message, Signature=signature, SigningAlgorithm='RSASSA_PKCS1_V1_5')
    return response['SignatureValid']