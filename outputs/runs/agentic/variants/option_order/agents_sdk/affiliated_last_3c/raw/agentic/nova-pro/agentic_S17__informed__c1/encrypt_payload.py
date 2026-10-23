import boto3

def encrypt_payload(plaintext, key_id):
    client = boto3.client('kms')
    response = client.encrypt(KeyId=key_id, Plaintext=plaintext)
    return response['CiphertextBlob']