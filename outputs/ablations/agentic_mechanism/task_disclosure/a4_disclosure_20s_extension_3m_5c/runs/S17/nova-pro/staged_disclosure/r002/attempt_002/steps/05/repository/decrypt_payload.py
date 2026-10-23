import boto3

def decrypt_payload(ciphertext_blob, key_id):
    kms_client = boto3.client('kms')
    response = kms_client.decrypt(
        CiphertextBlob=ciphertext_blob,
        KeyId=key_id
    )
    plaintext = response['Plaintext']
    return plaintext

if __name__ == '__main__':
    ciphertext = b'ciphertext-data'  # Replace with actual ciphertext
    key_id = 'alias/my-key'  # Replace with actual key ID or alias
    decrypted_payload = decrypt_payload(ciphertext, key_id)
    print(decrypted_payload.decode('utf-8'))