import boto3

kms = boto3.client('kms')

def encrypt_payload(plaintext):
    response = kms.encrypt(
        KeyId='alias/myKey',
        Plaintext=plaintext
    )
    return response['CiphertextBlob']