import boto3
import os
from typing import Tuple

def generate_data_key_and_encrypt(key_id: str, region: str = 'us-east-1') -> Tuple[bytes, bytes]:
    """
    Generates a data key and encrypts it using AWS KMS (envelope encryption).
    Returns the plaintext data key and the encrypted data key.
    """
    kms_client = boto3.client('kms', region_name=region)
    response = kms_client.generate_data_key(
        KeyId=key_id,
        KeySpec='AES_256' # or 'AES_128'
    )
    # The Plaintext field contains the data key, which you use to encrypt your data locally.
    # The CiphertextBlob contains the encrypted data key, which you store with your encrypted data.
    return response['Plaintext'], response['CiphertextBlob']

def decrypt_data_key(encrypted_data_key: bytes, region: str = 'us-east-1') -> bytes:
    """
    Decrypts an encrypted data key using AWS KMS.
    """
    kms_client = boto3.client('kms', region_name=region)
    response = kms_client.decrypt(
        CiphertextBlob=encrypted_data_key
    )
    return response['Plaintext']

if __name__ == '__main__':
    # This is example usage and should not be part of the final submission.
    # Replace with your actual KMS key ID.
    # Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION are set in environment variables.
    kms_key_id = os.environ.get("KMS_KEY_ID", "alias/MyKMSKey")
    
    # plaintext_data_key, encrypted_data_key = generate_data_key_and_encrypt(kms_key_id)
    # print(f"Plaintext Data Key (first 10 bytes): {plaintext_data_key[:10]}")
    # print(f"Encrypted Data Key (first 10 bytes): {encrypted_data_key[:10]}")
    
    # # Example of decrypting the data key
    # decrypted_data_key = decrypt_data_key(encrypted_data_key)
    # print(f"Decrypted Data Key (first 10 bytes): {decrypted_data_key[:10]}")
    # assert plaintext_data_key == decrypted_data_key
