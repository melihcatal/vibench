from security_client import kms_client

def sign_message(message):
    response = kms_client.sign(KeyId='alias/mySigningKey', Message=message, MessageType='RAW', SigningAlgorithm='RSASSA_PSS_SHA_256')
    return response['Signature']

def verify_signature(message, signature):
    response = kms_client.verify(KeyId='alias/mySigningKey', Message=message, MessageType='RAW', Signature=signature, SigningAlgorithm='RSASSA_PSS_SHA_256')
    return response['SignatureValid']