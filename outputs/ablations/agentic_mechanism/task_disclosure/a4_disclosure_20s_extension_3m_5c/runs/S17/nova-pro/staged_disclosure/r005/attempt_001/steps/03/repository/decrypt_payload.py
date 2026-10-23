import boto3

def decrypt_payload(ciphertext_blob, key_id):
    kms = boto3.client('kms')
    response = kms.decrypt(
        CiphertextBlob=ciphertext_blob,
        KeyId=key_id
    )
    return response['Plaintext']

if __name__ == '__main__':
    ciphertext = b'your_ciphertext_here'
    key_id = 'your_key_id_here'
    plaintext = decrypt_payload(ciphertext, key_id)
    print(plaintext.decode('utf-8'))