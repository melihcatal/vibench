import boto3

def decrypt_payload(ciphertext_blob, key_id):
    kms_client = boto3.client('kms')
    response = kms_client.decrypt(
        CiphertextBlob=ciphertext_blob,
        KeyId=key_id
    )
    return response['Plaintext']
