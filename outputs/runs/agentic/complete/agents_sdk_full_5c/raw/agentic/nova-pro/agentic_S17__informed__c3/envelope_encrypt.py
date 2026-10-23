import boto3

def envelope_encrypt(plaintext):
    client = boto3.client('kms')
    data_key = client.generate_data_key(KeyId='alias/myKey', KeySpec='AES_256')
    ciphertext = client.encrypt(KeyId=data_key['KeyId'], Plaintext=plaintext)['CiphertextBlob']
    return ciphertext, data_key['CiphertextBlob']