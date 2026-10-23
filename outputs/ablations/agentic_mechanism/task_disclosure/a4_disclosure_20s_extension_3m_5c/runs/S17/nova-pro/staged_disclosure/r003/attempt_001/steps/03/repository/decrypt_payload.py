import boto3

def decrypt_payload(ciphertext_blob):
    kms_client = boto3.client('kms')
    response = kms_client.decrypt(
        CiphertextBlob=ciphertext_blob
    )
    return response['Plaintext']

if __name__ == '__main__':
    # Example usage
    ciphertext_blob = b'example_ciphertext'
    plaintext = decrypt_payload(ciphertext_blob)
    print(plaintext)