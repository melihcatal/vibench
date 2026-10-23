import boto3

def encrypt_payload(plaintext, key_id):
    kms_client = boto3.client('kms')
    response = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext
    )
    return response['CiphertextBlob']
