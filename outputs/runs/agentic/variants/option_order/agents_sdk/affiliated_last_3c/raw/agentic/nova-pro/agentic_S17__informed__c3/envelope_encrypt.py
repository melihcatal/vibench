import boto3

def envelope_encrypt(data):
    client = boto3.client('kms')
    response = client.generate_data_key(KeyId='alias/example_key', KeySpec='AES_256')
    ciphertext = response['CiphertextBlob']
    plaintext_key = response['Plaintext']
    encrypted_data = encrypt_with_aes(data, plaintext_key)
    return ciphertext, encrypted_data

def encrypt_with_aes(data, key):
    from Crypto.Cipher import AES
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce + ciphertext + tag