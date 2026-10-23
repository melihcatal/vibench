import boto3

def envelope_encrypt(data_key):
    kms = boto3.client('kms')
    response = kms.encrypt(KeyId='alias/example_key', Plaintext=data_key)
    return response['CiphertextBlob']