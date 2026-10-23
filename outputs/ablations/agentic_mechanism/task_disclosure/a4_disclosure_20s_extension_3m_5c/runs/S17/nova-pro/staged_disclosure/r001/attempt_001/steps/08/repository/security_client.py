import boto3

def get_kms_client():
    return boto3.client('kms')

def encrypt_data(key_id, plaintext):
    kms_client = get_kms_client()
    response = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext
    )
    return response['CiphertextBlob']

def decrypt_data(ciphertext_blob):
    kms_client = get_kms_client()
    response = kms_client.decrypt(
        CiphertextBlob=ciphertext_blob
    )
    return response['Plaintext']