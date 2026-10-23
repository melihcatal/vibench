import boto3

def decrypt_payload(ciphertext_blob):
    kms_client = boto3.client('kms')
    response = kms_client.decrypt(
        CiphertextBlob=ciphertext_blob
    )
    return response['Plaintext']
