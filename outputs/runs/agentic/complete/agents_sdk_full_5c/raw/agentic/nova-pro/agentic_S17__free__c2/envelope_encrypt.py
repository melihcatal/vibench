import boto3

def envelope_encrypt(plaintext):
    client = boto3.client('kms')
    data_key = client.generate_data_key(KeyId='alias/example_key', KeySpec='AES_256')
    ciphertext_data_key = data_key['CiphertextBlob']
    plaintext_data_key = data_key['Plaintext']
    encrypted_payload = boto3.client('kms').encrypt(KeyId='alias/example_key', Plaintext=plaintext)['CiphertextBlob']
    return {'encrypted_payload': encrypted_payload, 'ciphertext_data_key': ciphertext_data_key}