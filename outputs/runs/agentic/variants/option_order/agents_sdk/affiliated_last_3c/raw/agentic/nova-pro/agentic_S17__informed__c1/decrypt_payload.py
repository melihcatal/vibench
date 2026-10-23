import boto3

def decrypt_payload(ciphertext, key_id):
    client = boto3.client('kms')
    response = client.decrypt(KeyId=key_id, CiphertextBlob=ciphertext)
    return response['Plaintext']