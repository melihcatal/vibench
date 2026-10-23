import boto3

kms = boto3.client('kms')

def envelope_encrypt(plaintext):
    data_key = kms.generate_data_key(
        KeyId='alias/myKey',
        KeySpec='AES_256'
    )
    encrypted_data_key = data_key['CiphertextBlob']
    plaintext_data_key = data_key['Plaintext']
    encrypted_payload = kms.encrypt(
        KeyId='alias/myKey',
        Plaintext=plaintext
    )
    return encrypted_data_key, encrypted_payload['CiphertextBlob']