import boto3

def envelope_encrypt(data):
    kms_client = boto3.client('kms')
    data_key = kms_client.generate_data_key(
        KeyId='alias/example_key',
        KeySpec='AES_256'
    )
    encrypted_data_key = data_key['CiphertextBlob']
    plaintext_data_key = data_key['Plaintext']
    encrypted_data = encrypt_data(data, plaintext_data_key)
    return encrypted_data_key, encrypted_data

def encrypt_data(data, key):
    from Crypto.Cipher import AES
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce + ciphertext + tag