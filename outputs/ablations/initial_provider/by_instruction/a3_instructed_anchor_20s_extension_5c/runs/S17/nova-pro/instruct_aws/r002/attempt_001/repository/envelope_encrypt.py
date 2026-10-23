import boto3

def envelope_encrypt(plaintext):
    kms_client = boto3.client('kms')
    data_key = kms_client.generate_data_key(
        KeyId='alias/example_key',
        KeySpec='AES_256'
    )
    ciphertext_data_key = data_key['CiphertextBlob']
    plaintext_data_key = data_key['Plaintext']
    encrypted_payload = kms_client.encrypt(
        KeyId='alias/example_key',
        Plaintext=plaintext
    )
    return {
        'encrypted_data_key': ciphertext_data_key,
        'encrypted_payload': encrypted_payload['CiphertextBlob']
    }