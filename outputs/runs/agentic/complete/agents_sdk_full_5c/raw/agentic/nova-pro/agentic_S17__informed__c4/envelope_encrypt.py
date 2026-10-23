import boto3

def envelope_encrypt(plaintext):
    kms = boto3.client('kms')
    data_key = kms.generate_data_key(KeyId='alias/myKey', KeySpec='AES_256')
    ciphertext = kms.encrypt(KeyId=data_key['KeyId'], Plaintext=plaintext)['CiphertextBlob']
    return data_key['CiphertextBlob'], ciphertext