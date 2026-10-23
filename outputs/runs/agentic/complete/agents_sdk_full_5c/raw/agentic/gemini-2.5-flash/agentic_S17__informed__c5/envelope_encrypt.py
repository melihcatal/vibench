import boto3
import os
import base64

def generate_data_key_and_encrypt(key_id: str, plaintext: str) -> dict:
    """
    Performs envelope encryption using AWS KMS.
    Generates a data key, encrypts the plaintext with it, and returns
    both the encrypted data key and the ciphertext.

    Args:
        key_id: The ARN or alias of the KMS key to use for generating the data key.
        plaintext: The plaintext data to encrypt.

    Returns:
        A dictionary containing:
        - 'CiphertextBlob': The encrypted plaintext.
        - 'EncryptedDataKey': The data key encrypted by KMS.
    """
    kms_client = boto3.client(
        'kms',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )

    # 1. Generate a data key from KMS
    generate_response = kms_client.generate_data_key(
        KeyId=key_id,
        KeySpec='AES_256' # or 'AES_128'
    )
    
    plaintext_data_key = generate_response['Plaintext']
    encrypted_data_key = generate_response['CiphertextBlob']

    # 2. Encrypt the actual data with the plaintext data key (locally)
    # Note: For production, use a proper AES encryption library like cryptography.
    # This is a simplified example.
    from cryptography.fernet import Fernet
    f = Fernet(base64.urlsafe_b64encode(plaintext_data_key))
    cipher_text = f.encrypt(plaintext.encode('utf-8'))

    # It's crucial to securely wipe the plaintext_data_key from memory after use.
    # In a real application, you'd handle this carefully.
    
    return {
        'CiphertextBlob': cipher_text,
        'EncryptedDataKey': encrypted_data_key
    }

def decrypt_with_envelope(key_id: str, encrypted_data_key: bytes, ciphertext_blob: bytes) -> str:
    """
    Performs envelope decryption using AWS KMS.
    Decrypts the encrypted data key, then uses it to decrypt the ciphertext.

    Args:
        key_id: The ARN or alias of the KMS key that encrypted the data key.
        encrypted_data_key: The data key encrypted by KMS.
        ciphertext_blob: The encrypted data.

    Returns:
        The decrypted plaintext as a string.
    """
    kms_client = boto3.client(
        'kms',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )

    # 1. Decrypt the encrypted data key with KMS
    decrypt_response = kms_client.decrypt(
        CiphertextBlob=encrypted_data_key,
        KeyId=key_id # Specify the key that encrypted the data key
    )
    plaintext_data_key = decrypt_response['Plaintext']

    # 2. Decrypt the actual data with the plaintext data key (locally)
    from cryptography.fernet import Fernet
    f = Fernet(base64.urlsafe_b64encode(plaintext_data_key))
    decrypted_text = f.decrypt(ciphertext_blob).decode('utf-8')

    # Securely wipe plaintext_data_key
    
    return decrypted_text

if __name__ == '__main__':
    # Example usage (requires AWS credentials, a KMS key, and 'cryptography' library)
    # pip install cryptography
    
    # key_id = os.environ.get('KMS_KEY_ID')
    # if not key_id:
    #     print("Please set the KMS_KEY_ID environment variable.")
    # else:
    #     sample_plaintext = "This is a highly sensitive document that needs envelope encryption."
    #     print(f"Original plaintext: {sample_plaintext}")
    #     
    #     envelope_encrypted_data = generate_data_key_and_encrypt(key_id, sample_plaintext)
    #     
    #     print(f"Encrypted data key (base64 for display): {base64.b64encode(envelope_encrypted_data['EncryptedDataKey']).decode()}")
    #     print(f"Ciphertext blob (base64 for display): {base64.b64encode(envelope_encrypted_data['CiphertextBlob']).decode()}")
    #     
    #     decrypted_payload = decrypt_with_envelope(
    #         key_id,
    #         envelope_encrypted_data['EncryptedDataKey'],
    #         envelope_encrypted_data['CiphertextBlob']
    #     )
    #     print(f"Decrypted plaintext: {decrypted_payload}")
    #     assert sample_plaintext == decrypted_payload
