import boto3

def envelope_encrypt(plaintext):
    # Initialize a boto3 client for AWS KMS
    kms_client = boto3.client('kms', region_name='us-west-2')

    # Generate a data key using AWS KMS
    response = kms_client.generate_data_key(
        KeyId='alias/example_key',
        KeySpec='AES_256'
    )

    # Extract the plaintext data key and the ciphertext blob
    data_key_plaintext = response['Plaintext']
    data_key_ciphertext = response['CiphertextBlob']

    # Encrypt the plaintext using the data key
    from Crypto.Cipher import AES
    cipher = AES.new(data_key_plaintext, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))

    # Return the encrypted data key and the ciphertext
    return {
        'CiphertextBlob': data_key_ciphertext,
        'Ciphertext': cipher.nonce + tag + ciphertext
    }

if __name__ == '__main__':
    plaintext = 'Sensitive data to encrypt'
    encrypted_data = envelope_encrypt(plaintext)
    print(encrypted_data)