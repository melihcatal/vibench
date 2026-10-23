import boto3

def get_kms_client():
    return boto3.client('kms')

def encrypt(plaintext, key_id):
    kms_client = get_kms_client()
    response = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext
    )
    return response['CiphertextBlob']

def decrypt(ciphertext, key_id):
    kms_client = get_kms_client()
    response = kms_client.decrypt(
        KeyId=key_id,
        CiphertextBlob=ciphertext
    )
    return response['Plaintext']

def generate_data_key(key_id):
    kms_client = get_kms_client()
    response = kms_client.generate_data_key(
        KeyId=key_id,
        KeySpec='AES_256'
    )
    return response['Plaintext'], response['CiphertextBlob']