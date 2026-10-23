import boto3

def envelope_encrypt(plaintext):
    kms_client = boto3.client('kms', region_name='us-west-2')
    data_key = kms_client.generate_data_key(KeyId='alias/example_key', KeySpec='AES_256')
    ciphertext_data_key = data_key['CiphertextBlob']
    encrypted_data = kms_client.encrypt(
       KeyId='alias/example_key',
       Plaintext=plaintext,
       EncryptionContext={'Purpose': 'Envelope Encryption'}
    )
    return {
        'CiphertextBlob': encrypted_data['CiphertextBlob'],
        'CiphertextDataKey': ciphertext_data_key
    }

if __name__ == '__main__':
    plaintext = 'Sensitive data to be encrypted'
    encrypted = envelope_encrypt(plaintext)
    print(encrypted)