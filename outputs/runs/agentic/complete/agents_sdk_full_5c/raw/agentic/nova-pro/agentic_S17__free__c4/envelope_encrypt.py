import boto3

def envelope_encrypt(data):
    kms = boto3.client('kms')
    response = kms.generate_data_key(KeyId='alias/myKey', KeySpec='AES_256')
    encrypted_data_key = response['CiphertextBlob']
    plaintext_data_key = response['Plaintext']
    # Encrypt data using the plaintext data key
    #... (encryption logic here)
    return encrypted_data_key, encrypted_data