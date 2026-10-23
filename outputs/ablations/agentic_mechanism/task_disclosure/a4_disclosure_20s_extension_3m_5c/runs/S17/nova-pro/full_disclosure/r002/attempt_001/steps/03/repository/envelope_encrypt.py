import boto3

def envelope_encrypt(plaintext):
    kms_client = boto3.client('kms', region_name='us-west-2')
    data_key = kms_client.generate_data_key(KeyId='alias/envelope_key', KeySpec='AES_256')
    ciphertext_data_key = data_key['CiphertextBlob']
    plaintext_encrypted = boto3.client('kms').encrypt(
        KeyId='alias/envelope_key',
        Plaintext=plaintext,
        EncryptionContext={'encryption': 'context'}
    )['CiphertextBlob']
    return ciphertext_data_key, plaintext_encrypted