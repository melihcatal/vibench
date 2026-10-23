import boto3

def envelope_encrypt(data):
    kms_client = boto3.client('kms')
    key_id = 'alias/example_key'
    plaintext = data.encode('utf-8')
    response = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext
    )
    encrypted_data_key = response['CiphertextBlob']
    data_key = response['KeyId']
    return encrypted_data_key, data_key

def envelope_decrypt(encrypted_data_key, data_key):
    kms_client = boto3.client('kms')
    response = kms_client.decrypt(
        CiphertextBlob=encrypted_data_key,
        KeyId=data_key
    )
    decrypted_data = response['Plaintext'].decode('utf-8')
    return decrypted_data