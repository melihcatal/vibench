import boto3

def configure_kms_client(region_name='us-west-2'):
    return boto3.client('kms', region_name=region_name)

def encrypt_data(client, plaintext):
    response = client.encrypt(
        KeyId='alias/example_key',
        Plaintext=plaintext
    )
    return response['CiphertextBlob']

def decrypt_data(client, ciphertext):
    response = client.decrypt(
        CiphertextBlob=ciphertext
    )
    return response['Plaintext']