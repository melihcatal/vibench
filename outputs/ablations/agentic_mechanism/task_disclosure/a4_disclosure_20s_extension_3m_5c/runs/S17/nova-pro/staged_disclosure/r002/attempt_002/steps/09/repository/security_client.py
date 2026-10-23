import boto3

def configure_kms_client(region_name='us-west-2'):
    session = boto3.Session(region_name=region_name)
    kms_client = session.client('kms')
    return kms_client

def encrypt_data(kms_client, plaintext):
    response = kms_client.encrypt(
        KeyId='alias/example_key',
        Plaintext=plaintext
    )
    return response['CiphertextBlob']

def decrypt_data(kms_client, ciphertext):
    response = kms_client.decrypt(
        CiphertextBlob=ciphertext
    )
    return response['Plaintext'].decode('utf-8')
