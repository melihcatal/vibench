import boto3
import os

def decrypt_payload(ciphertext_blob: bytes, region: str = 'us-east-1') -> str:
    """
    Decrypts a ciphertext payload using AWS KMS.
    """
    kms_client = boto3.client('kms', region_name=region)
    response = kms_client.decrypt(
        CiphertextBlob=ciphertext_blob
    )
    return response['Plaintext'].decode('utf-8')

if __name__ == '__main__':
    # This is example usage and should not be part of the final submission.
    # Replace with your actual ciphertext blob.
    # Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION are set in environment variables.
    
    # For demonstration, assume 'encrypted_data' came from encrypt_payload.py
    # from encrypt_payload import encrypt_payload
    # kms_key_id = os.environ.get("KMS_KEY_ID", "alias/MyKMSKey")
    # example_plaintext = "This is a secret message to be decrypted."
    # encrypted_data_for_decrypt = encrypt_payload(example_plaintext, kms_key_id)
    
    # decrypted_text = decrypt_payload(encrypted_data_for_decrypt)
    # print(f"Decrypted text: {decrypted_text}")
