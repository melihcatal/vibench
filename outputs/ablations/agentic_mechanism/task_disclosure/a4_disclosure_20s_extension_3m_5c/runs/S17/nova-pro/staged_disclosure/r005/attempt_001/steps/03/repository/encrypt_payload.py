import boto3

def encrypt_payload(plaintext, key_id):
    kms = boto3.client('kms')
    response = kms.encrypt(
        KeyId=key_id,
        Plaintext=plaintext
    )
    return response['CiphertextBlob']

if __name__ == '__main__':
    plaintext = 'This is a plaintext message to encrypt.'
    key_id = 'alias/myEncryptionKey'
    encrypted_payload = encrypt_payload(plaintext, key_id)
    print(f'Encrypted payload: {encrypted_payload}')
