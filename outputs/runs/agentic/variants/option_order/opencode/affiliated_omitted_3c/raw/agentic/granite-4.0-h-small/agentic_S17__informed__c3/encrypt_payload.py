import os
import hashlib
from cryptography.fernet import Fernet

# AWS KMS integration example
# Requires boto3 and proper AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
import boto3
from botocore.exceptions import ClientError

# Local helper imports
from security_client import KeyManagementClient
from security_models import PlaintextPayload, CiphertextPayload


class AES256Encryptor:
    """Encrypts plaintext using AES-256 encryption."""

    def __init__(self, key: bytes):
        self.fernet = Fernet(key)

    def encrypt(self, plaintext: str) -> bytes:
        """Encrypts plaintext and returns base64 encoded ciphertext."""
        return self.fernet.encrypt(plaintext.encode())


class KMSCrypto:
    """Uses AWS KMS to generate a data key and encrypt/decrypt payloads."""

    def __init__(self, region_name="us-east-1"):
        self.kms_client = boto3.client("kms", region_name=region_name)
        self.data_key = None

    def generate_data_key(self, key_id: str) -> bytes:
        """Generate a new data key and cache it."""
        try:
            response = self.kms_client.generate_data_key(
                KeyId=key_id, KeySpec="AES_256"
            )
            plaintext_key = response["Plaintext"]  # Already bytes
            self.data_key = plaintext_key
            return plaintext_key
        except ClientError as e:
            raise RuntimeError(f"Failed to generate data key: {e}")

    def encrypt_payload(self, plaintext: str) -> CiphertextPayload:
        """Encrypt plaintext using generated data key."""
        if not self.data_key:
            raise RuntimeError(
                "Data key not initialized. Call generate_data_key first."
            )
        aes_encryptor = AES256Encryptor(self.data_key)
        ciphertext = aes_encryptor.encrypt(plaintext)
        return CiphertextPayload(ciphertext=ciphertext, key_id=self.data_key.hex())

    def decrypt_payload(
        self, ciphertext_payload: CiphertextPayload
    ) -> PlaintextPayload:
        """Decrypt ciphertext using cached data key."""
        if not self.data_key:
            raise RuntimeError(
                "Data key not initialized. Call generate_data_key first."
            )
        aes_encryptor = AES256Encryptor(self.data_key)
        plaintext = aes_encryptor.encrypt(
            ciphertext_payload.ciphertext.decode()
        ).decode()
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
    plain = "Hello, world! This is a secret message."
    ct_payload = kms.encrypt_payload(plain)
    print("Encrypted payload (base64):", ct_payload.ciphertext)
    pt_payload = kms.decrypt_payload(ct_payload)
    print("Decrypted plaintext:", pt_payload.plaintext)
