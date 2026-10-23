from security_client import get_kms_client

def sign_or_verify_key(data, signature):
    client = get_kms_client()
    response = client.verify(KeyId='alias/mySigningKey', Message=data, Signature=signature, SigningAlgorithm='RSASSA_PKCS1_V1_5')
    return response['SignatureValid']