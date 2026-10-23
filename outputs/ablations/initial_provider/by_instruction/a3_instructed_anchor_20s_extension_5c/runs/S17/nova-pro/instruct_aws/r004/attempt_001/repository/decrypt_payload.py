import boto3

def decrypt_payload(ciphertext):
    client = boto3.client('kms')
    response = client.decrypt(
        CiphertextBlob=ciphertext
    )
    return response['Plaintext']