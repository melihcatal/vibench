import boto3

def encrypt_data(plaintext):
    kms = boto3.client('kms')
    response = kms.encrypt(
        KeyId='alias/myKey',
        Plaintext=plaintext
    )
    return response['CiphertextBlob']

def decrypt_data(ciphertext):
    kms = boto3.client('kms')
    response = kms.decrypt(
        CiphertextBlob=ciphertext
    )
    return response['Plaintext']

if __name__ == '__main__':
    plaintext = b'This is a test message.'
    ciphertext = encrypt_data(plaintext)
    decrypted_data = decrypt_data(ciphertext)
    print(f'Decrypted data: {decrypted_data}')
