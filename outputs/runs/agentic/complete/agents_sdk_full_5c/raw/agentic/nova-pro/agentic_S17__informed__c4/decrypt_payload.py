import boto3

def decrypt_payload(ciphertext):
    kms = boto3.client('kms')
    response = kms.decrypt(CiphertextBlob=ciphertext)
    return response['Plaintext']