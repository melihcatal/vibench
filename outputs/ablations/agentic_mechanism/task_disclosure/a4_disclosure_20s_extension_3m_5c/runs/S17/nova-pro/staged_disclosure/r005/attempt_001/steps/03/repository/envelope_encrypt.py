import boto3

def envelope_encrypt(plaintext):
    kms_client = boto3.client('kms', region_name='us-west-2')
    key_id = 'alias/myEncryptionKey'

    # Generate a data key
    data_key_plaintext = kms_client.generate_data_key(KeyId=key_id, KeySpec='AES_256')['Plaintext']

    # Encrypt the plaintext with the data key
    ciphertext = kms_client.encrypt(KeyId=key_id, Plaintext=plaintext)['CiphertextBlob']

    # Encrypt the data key with the master key
    encrypted_data_key = kms_client.encrypt(KeyId=key_id, Plaintext=data_key_plaintext)['CiphertextBlob']

    return ciphertext, encrypted_data_key

def envelope_decrypt(ciphertext, encrypted_data_key):
    kms_client = boto3.client('kms', region_name='us-west-2')

    # Decrypt the data key
    data_key_plaintext = kms_client.decrypt(CiphertextBlob=encrypted_data_key)['Plaintext']

    # Decrypt the ciphertext with the data key
    plaintext = kms_client.decrypt(CiphertextBlob=ciphertext, EncryptionAlgorithm='SYMMETRIC_DEFAULT', KeyId='alias/myEncryptionKey')['Plaintext']

    return plaintext