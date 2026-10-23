import boto3

def envelope_encrypt(data):
    client = boto3.client('kms')
    response = client.generate_data_key(KeyId='alias/example_key', KeySpec='AES_256')
    plaintext_data_key = response['Plaintext']
    ciphertext_data_key = response['CiphertextBlob']
    encrypted_data = encrypt_payload(data)
    return {'encrypted_data': encrypted_data, 'ciphertext_data_key': ciphertext_data_key}