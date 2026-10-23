import boto3

def envelope_encrypt(plaintext):
    client = boto3.client('kms')
    data_key = client.generate_data_key(KeyId='alias/example_key', KeySpec='AES_256')
    ciphertext_data_key = data_key['CiphertextBlob']
    plaintext_data_key = data_key['Plaintext']
    encrypted_payload = some_encryption_function(plaintext, plaintext_data_key)
    return ciphertext_data_key, encrypted_payload