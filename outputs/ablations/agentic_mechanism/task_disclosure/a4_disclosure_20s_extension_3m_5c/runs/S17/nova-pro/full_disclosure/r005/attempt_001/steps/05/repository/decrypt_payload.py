import boto3

def decrypt_payload(ciphertext_blob, key_id):
    kms_client = boto3.client('kms')
    response = kms_client.decrypt(
        CiphertextBlob=ciphertext_blob,
        KeyId=key_id
    )
    return response['Plaintext']

if __name__ == '__main__':
    # Example usage
    ciphertext_blob = b'ciphertext'
    key_id = 'alias/myKey'
    plaintext = decrypt_payload(ciphertext_blob, key_id)
    print(plaintext)