import boto3

def envelope_encrypt(data_key):
    client = boto3.client('kms')
    response = client.encrypt(KeyId='alias/example-key', Plaintext=data_key)
    return response['CiphertextBlob']