import boto3

kms = boto3.client('kms')

def decrypt_payload(ciphertext):
    response = kms.decrypt(
        CiphertextBlob=ciphertext
    )
    return response['Plaintext']