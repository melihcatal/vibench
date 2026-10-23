import boto3

def encrypt_payload(plaintext):
    kms = boto3.client('kms')
    response = kms.encrypt(KeyId='alias/myKey', Plaintext=plaintext)
    return response['CiphertextBlob']