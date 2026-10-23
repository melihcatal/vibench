import boto3

def decrypt_payload(ciphertext_blob):
    kms_client = boto3.client('kms', region_name='us-west-2')
    response = kms_client.decrypt(
        CiphertextBlob=ciphertext_blob
    )
    plaintext = response['Plaintext']
    return plaintext

if __name__ == '__main__':
    with open('encrypted_payload.bin', 'rb') as f:
        encrypted_payload = f.read()
    decrypted_payload = decrypt_payload(encrypted_payload)
    with open('decrypted_payload.txt', 'wb') as f:
        f.write(decrypted_payload)