import boto3
import os
from security_client import get_kms_client
import base64

def envelope_encrypt(plaintext: str, key_id: str):
    """
    Implements envelope encryption using AWS KMS.
    Generates a data key from KMS and uses it to encrypt the plaintext locally.
    The data key itself is encrypted by KMS.
    """
    kms_client = get_kms_client()
    try:
        # 1. Generate a data key from KMS
        response = kms_client.generate_data_key(
            KeyId=key_id,
            KeySpec='AES_256' # Specifies the type of data key to generate
        )
        encrypted_data_key = response['CiphertextBlob']
        plaintext_data_key = response['Plaintext']

        # 2. Use the plaintext data key to encrypt the actual data (local encryption)
        # Note: For production, use a proper cryptographic library like cryptography.io
        # This is a simplified example.
        from cryptography.fernet import Fernet
        
        # Fernet key must be URL-safe base64-encoded
        fernet_key = base64.urlsafe_b64encode(plaintext_data_key)
        f = Fernet(fernet_key)
        locally_encrypted_payload = f.encrypt(plaintext.encode('utf-8'))

        # 3. Return the encrypted data key and the locally encrypted payload
        return {
            "encrypted_data_key": encrypted_data_key,
            "locally_encrypted_payload": locally_encrypted_payload
        }
    except Exception as e:
        print(f"Error during envelope encryption: {e}")
        raise

if __name__ == '__main__':
    # Example Usage
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME, AWS_KMS_KEY_ID must be set
    kms_key_id = os.environ.get("AWS_KMS_KEY_ID", "alias/MyEnvelopeKey")
    example_plaintext = "This is sensitive data for envelope encryption."

    try:
        envelope_encrypted_result = envelope_encrypt(example_plaintext, kms_key_id)
        print(f"Encrypted Data Key (hex): {envelope_encrypted_result['encrypted_data_key'].hex()}")
        print(f"Locally Encrypted Payload: {envelope_encrypted_result['locally_encrypted_payload']}")
    except Exception as e:
        print(f"Envelope encryption failed: {e}")
