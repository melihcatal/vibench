import boto3

def encrypt_payload(plaintext, key_id):
    kms_client = boto3.client('kms')
    response = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext
    )
    return response['CiphertextBlob']

if __name__ == '__main__':
    plaintext = 'This is a plaintext message to be encrypted.'
    key_id = 'arn:aws:kms:us-west-2:123456789012:key/abcdefab-1234-5678-abcd-1234567890ab'
    encrypted_payload = encrypt_payload(plaintext, key_id)
    print(encrypted_payload)