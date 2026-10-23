import boto3

def envelope_encrypt(data):
    client = boto3.client('kms', region_name='us-west-2')
    key_id = 'arn:aws:kms:us-west-2:123456789012:key/abcdefgh-1234-5678-9012-abcdefghijkl'
    response = client.generate_data_key(KeyId=key_id, KeySpec='AES_256')
    plaintext_key = response['Plaintext']
    encrypted_data_key = response['CiphertextBlob']
    from Crypto.Cipher import AES
    cipher = AES.new(plaintext_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return {'encrypted_data_key': encrypted_data_key, 'ciphertext': ciphertext, 'tag': tag, 'nonce': cipher.nonce}