import boto3
import os

def decrypt_payload(ciphertext_blob: bytes) -> str:
    """
    Decrypts a ciphertext payload using AWS KMS.

    Args:
        ciphertext_blob: The ciphertext blob to decrypt.

    Returns:
        The decrypted plaintext as a string.
    """
    kms_client = boto3.client(
        'kms',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )
    response = kms_client.decrypt(
        CiphertextBlob=ciphertext_blob
    )
    return response['Plaintext'].decode('utf-8')

if __name__ == '__main__':
    # Example usage (requires AWS credentials and a KMS key with decryption permissions)
    # For a full example, you would typically encrypt first, then decrypt.
    # This example assumes you have an encrypted blob.
    # To run this, you'd need the ciphertext_blob from encrypt_payload.py
    
    # import base64
    # from encrypt_payload import encrypt_payload
    # key_id = os.environ.get('KMS_KEY_ID')
    # if not key_id:
    #     print("Please set the KMS_KEY_ID environment variable.")
    # else:
    #     sample_plaintext = "This is another secret message for decryption."
    #     print(f"Original plaintext for encryption: {sample_plaintext}")
    #     encrypted_blob = encrypt_payload(key_id, sample_plaintext)
    #     print(f"Encrypted blob (base64 for display): {base64.b64encode(encrypted_blob).decode()}")
    #     
    #     decrypted_text = decrypt_payload(encrypted_blob)
    #     print(f"Decrypted plaintext: {decrypted_text}")
    #     assert sample_plaintext == decrypted_text
