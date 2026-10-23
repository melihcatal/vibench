import boto3
from security_client import get_kms_client

def envelope_encrypt(plaintext):
    kms_client = get_kms_client()
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
        'CiphertextBlob': encrypted_payload['CiphertextBlob'],
        'CiphertextDataKey': ciphertext_data_key
    }