import boto3

def encrypt_data(plaintext):
    kms_client = boto3.client('kms')
    key_id = 'alias/my_key'
    response = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext
    )
    return response['CiphertextBlob']

def decrypt_data(ciphertext):
    kms_client = boto3.client('kms')
    response = kms_client.decrypt(
        CiphertextBlob=ciphertext
    )
    return response['Plaintext']

if __name__ == '__main__':
    plaintext = b'This is a secret message.'
    ciphertext = encrypt_data(plaintext)
    print('Encrypted data:', ciphertext)
    decrypted_data = decrypt_data(ciphertext)
    print('Decrypted data:', decrypted_data.decode())