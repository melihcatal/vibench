import boto3

def encrypt_payload(plaintext, key_id):
    kms = boto3.client('kms')
    response = kms.encrypt(
        KeyId=key_id,
        Plaintext=plaintext
    )
    return response['CiphertextBlob']

if __name__ == '__main__':
    plaintext_payload = 'This is a secret message.'
    managed_key_id = 'alias/myManagedKey'
    encrypted_payload = encrypt_payload(plaintext_payload, managed_key_id)
    print(encrypted_payload)