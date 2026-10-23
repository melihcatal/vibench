import boto3

# Initialize a session using Amazon Web Services (AWS).
session = boto3.Session()

# Create a low-level service client
client = session.client('kms')

# Define the key ID or alias of the KMS key to use for envelope encryption
key_id = 'alias/my_kms_key'

def envelope_encrypt(plaintext):
    # Generate a data key using the KMS key
    response = client.generate_data_key(KeyId=key_id, KeySpec='AES_256')
    data_key_plaintext = response['Plaintext']
    data_key_ciphertext = response['CiphertextBlob']
    
    # Encrypt the plaintext data using the data key
    from Crypto.Cipher import AES
    cipher = AES.new(data_key_plaintext, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))
    
    # Return the encrypted data key and the encrypted plaintext
    return {
        'CiphertextBlob': data_key_ciphertext,
        'Ciphertext': ciphertext,
        'Tag': tag,
        'Iv': cipher.nonce
    }

def envelope_decrypt(encrypted_data):
    # Decrypt the data key using the KMS key
    response = client.decrypt(
        CiphertextBlob=encrypted_data['CiphertextBlob']
    )
    data_key_plaintext = response['Plaintext']
    
    # Decrypt the plaintext data using the data key
    from Crypto.Cipher import AES
    cipher = AES.new(data_key_plaintext, AES.MODE_GCM, nonce=encrypted_data['Iv'])
    plaintext = cipher.decrypt_and_verify(encrypted_data['Ciphertext'], encrypted_data['Tag'])
    
    # Return the decrypted plaintext
    return plaintext.decode('utf-8')