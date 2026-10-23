import boto3

def envelope_encrypt(plaintext):
    kms_client = boto3.client('kms', region_name='us-west-2')
    data_key = kms_client.generate_data_key(KeyId='alias/example_key', KeySpec='AES_256')
    ciphertext_blob = data_key['CiphertextBlob']
    plaintext_encrypted = kms_client.encrypt(
       KeyId='alias/example_key',
       Plaintext=plaintext
    )
    return {
        'CiphertextBlob': ciphertext_blob,
        'EncryptedDataKey': plaintext_encrypted['CiphertextBlob']
    }
