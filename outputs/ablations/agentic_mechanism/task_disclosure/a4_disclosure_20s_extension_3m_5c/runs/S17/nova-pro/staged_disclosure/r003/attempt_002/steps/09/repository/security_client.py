import boto3

def create_kms_client():
    kms_client = boto3.client('kms')
    return kms_client

def encrypt_data(kms_client, plaintext):
    response = kms_client.encrypt(
        KeyId='alias/example_key',
        Plaintext=plaintext
    )
    return response['CiphertextBlob']

def decrypt_data(kms_client, ciphertext_blob):
    response = kms_client.decrypt(
        CiphertextBlob=ciphertext_blob
    )
    return response['Plaintext']