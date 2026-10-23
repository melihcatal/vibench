import boto3

def encrypt_payload(plaintext):
    kms_client = boto3.client('kms', region_name='us-west-2')
    key_id = 'alias/myEncryptionKey'
    response = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext
    )
    return response['CiphertextBlob']

if __name__ == '__main__':
    plaintext = 'This is a plaintext message to be encrypted.'
    encrypted_payload = encrypt_payload(plaintext)
    print(f'Encrypted Payload: {encrypted_payload}')
