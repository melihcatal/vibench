import boto3

def envelope_encrypt(data):
    client = boto3.client('kms')
    response = client.generate_data_key(KeyId='alias/example_key', KeySpec='AES_256')
    plaintext_data_key = response['Plaintext']
    encrypted_data_key = response['CiphertextBlob']
    encrypted_data = client.encrypt(KeyId='alias/example_key', Plaintext=data)['CiphertextBlob']
    return encrypted_data_key, encrypted_data