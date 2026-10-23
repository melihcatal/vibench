import boto3

def envelope_encrypt(plaintext):
    client = boto3.client('kms')
    data_key = client.generate_data_key(
        KeyId='alias/example_key',
        KeySpec='AES_256'
    )
    encrypt_client = boto3.client('kms')
    encrypted_data_key = encrypt_client.encrypt(
        KeyId='alias/example_key',
        Plaintext=data_key['Plaintext']
    )['CiphertextBlob']
    ciphertext = encrypt_client.encrypt(
        KeyId='alias/example_key',
        Plaintext=plaintext,
        EncryptionContext={'aws:example': 'context'}
    )['CiphertextBlob']
    return encrypted_data_key, ciphertext