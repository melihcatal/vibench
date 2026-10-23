import boto3

def encrypt_data(plaintext):
    kms_client = boto3.client('kms', region_name='us-west-2')
    key_id = 'alias/example-key'
    response = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext
    )
    return response['CiphertextBlob']

def decrypt_data(ciphertext):
    kms_client = boto3.client('kms', region_name='us-west-2')
    response = kms_client.decrypt(
        CiphertextBlob=ciphertext
    )
    return response['Plaintext']

if __name__ == '__main__':
    data_to_encrypt = b'This is some sensitive data.'
    encrypted_data = encrypt_data(data_to_encrypt)
    print('Encrypted data:', encrypted_data)
    decrypted_data = decrypt_data(encrypted_data)
    print('Decrypted data:', decrypted_data.decode('utf-8'))