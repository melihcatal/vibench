import boto3

def envelope_encrypt(plaintext):
    kms_client = boto3.client('kms', region_name='us-west-2')
    data_key = kms_client.generate_data_key(KeyId='alias/example-key', KeySpec='AES_256')
    ciphertext_blob = kms_client.encrypt(KeyId='alias/example-key', Plaintext=plaintext, EncryptionContext={'Purpose': 'Envelope Encryption'})['CiphertextBlob']
    encrypted_data_key = data_key['CiphertextBlob']
    return {'CiphertextBlob': ciphertext_blob, 'EncryptedDataKey': encrypted_data_key}
