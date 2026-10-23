import boto3

def encrypt_payload(plaintext, key_id):
    kms_client = boto3.client('kms')
    response = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext
    )
    return response['CiphertextBlob']

if __name__ == '__main__':
    # Example usage
    plaintext = 'This is a secret message'
    key_id = 'alias/myEncryptionKey'
    ciphertext = encrypt_payload(plaintext, key_id)
    print(f'Encrypted payload: {ciphertext}')
