import boto3

def encrypt_payload(plaintext):
    client = boto3.client('kms')
    response = client.encrypt(KeyId='alias/myKey', Plaintext=plaintext)
    return response['CiphertextBlob']