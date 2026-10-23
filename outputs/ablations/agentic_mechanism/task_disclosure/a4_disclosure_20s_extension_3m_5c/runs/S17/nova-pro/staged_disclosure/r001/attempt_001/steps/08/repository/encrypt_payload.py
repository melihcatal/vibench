import boto3

def encrypt_payload(plaintext):
    kms_client = boto3.client('kms')
    key_id = 'alias/myManagedKey'
    response = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext
    )
    return response['CiphertextBlob']

if __name__ == '__main__':
    plaintext = 'This is a secret message.'
    encrypted_payload = encrypt_payload(plaintext)
    print(f'Encrypted payload: {encrypted_payload}')
