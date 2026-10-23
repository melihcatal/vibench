import boto3

def decrypt_payload(ciphertext):
    client = boto3.client('kms', region_name='us-west-2')
    response = client.decrypt(CiphertextBlob=ciphertext)
    return response['Plaintext']