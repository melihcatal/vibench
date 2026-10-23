import boto3

def envelope_encrypt(data_key, plaintext):
    client = boto3.client('kms')
    response = client.encrypt(KeyId=data_key, Plaintext=plaintext)
    return response['CiphertextBlob']