import boto3

def envelope_encrypt(plaintext):
    kms_client = boto3.client('kms', region_name='us-west-2')
    data_key = kms_client.generate_data_key(KeyId='alias/example_key', KeySpec='AES_256')
    ciphertext_blob = data_key['CiphertextBlob']
    plaintext_key = data_key['Plaintext']
    encrypted_data_key = kms_client.encrypt(
        KeyId='alias/example_key',
        Plaintext=plaintext_key
    )['CiphertextBlob']
    encrypted_data = boto3.client('kms').encrypt(
        KeyId='alias/example_key',
        Plaintext=plaintext
    )['CiphertextBlob']
    return {
        'encrypted_data_key': encrypted_data_key,
        'encrypted_data': encrypted_data,
        'ciphertext_blob': ciphertext_blob
    }

if __name__ == '__main__':
    plaintext = 'Sensitive data to encrypt'
    encrypted = envelope_encrypt(plaintext)
    print(encrypted)