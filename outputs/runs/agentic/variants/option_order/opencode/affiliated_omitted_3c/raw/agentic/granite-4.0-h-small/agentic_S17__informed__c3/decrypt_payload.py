import os
import base64
from cryptography.fernet import Fernet

# AWS KMS integration example
# Requires boto3 and proper AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
import boto3
from botocore.exceptions import ClientError

# Local helper imports
from security_client import KeyManagementClient
from security_models import PlaintextPayload, CiphertextPayload

class AES256Decryptor:
    """Decrypts ciphertext using AES-256 encryption."""
    def __init__(self, key: bytes):
        self.fernet = Fernet(key)

    def decrypt(self, ciphertext: bytes) -> str:
        """Decrypts ciphertext and returns plaintext."""
        return self.fernet.decrypt(ciphertext).decode()

class KMSCrypto:
    """Uses AWS KMS to generate a data key and encrypt/decrypt payloads."""
    def __init__(self, region_name="us-east-1"):
        self.kms_client = boto3.client("kms", region_name=region_name)
        self.data_key = None

    def generate_data_key(self, key_id: str) -> bytes:
        """Generate a new data key and cache it."""
        try:
            response = self.kms_client.generate_data_key(
                KeyId=key_id,
                KeySpec="AES_256"
            )
            plaintext_key = response["Plaintext"]  # Already bytes
            self.data_key = plaintext_key
            return plaintext_key
        except ClientError as e:
            raise RuntimeError(f"Failed to generate data key: {e}")

    def decrypt_payload(self, ciphertext_payload: CiphertextPayload) -> PlaintextPayload:
        """Decrypt ciphertext using cached data key."""
        if not self.data_key:
            raise RuntimeError("Data key not initialized. Call generate_data_key first.")
        aes_decryptor = AES256Decryptor(self.data_key)
        plaintext = aes_decryptor.decrypt(ciphertext_payload.ciphertext)
        return PlaintextPayload(plaintext=plaintext)

# Helper to load key identifier from environment
KEY_ID = os.getenv("AWS_KMS_KEY_ID")
if not KEY_ID:
    raise RuntimeError("Set AWS_KMS_KEY_ID environment variable before running.")

# Initialize KMS client
kms = KMSCrypto(region_name="us-east-1")
try:
    kms.generate_data_key(KEY_ID)
except RuntimeError as e:
    print(e)
    raise

# Example usage
if __name__ == "__main__":
    # Assume ciphertext was produced by encrypt_payload.py
    # For demonstration, we reuse the same KEY_ID and generate a new data key – in practice keep the original key
    ct_payload = CiphertextPayload(
        ciphertext=b64=b"<BASE64_CIPHERTEXT_HERE>",
        key_id=KEY_ID
    )
    pt_payload = kms.decrypt_payload(ct_payload)
    print("Decrypted plaintext:", pt_payload.plaintext)
