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
    encrypted_data = encrypt_client.encrypt(
        KeyId='alias/example_key',
        Plaintext=plaintext
    )['CiphertextBlob']
    return {
        'EncryptedDataKey': encrypted_data_key,
        'CiphertextBlob': encrypted_data
    }