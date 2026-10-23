import os
import base64
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# AWS KMS integration example
# Requires boto3 and proper AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
import boto3
from botocore.exceptions import ClientError

# Local helper imports
from security_client import KeyManagementClient
from security_models import PlaintextPayload, CiphertextPayload


class EnvelopeEncryptor:
    """Performs envelope encryption using AWS KMS for key management and AES for content encryption."""

    def __init__(self, region_name="us-east-1"):
        self.kms_client = boto3.client("kms", region_name=region_name)
        self.data_key = None
        self.ciphertext_blob = None

    def generate_data_key(self, key_id: str) -> bytes:
        """Generate a new data key via KMS and cache plaintext key."""
        response = self.kms_client.generate_data_key(KeyId=key_id, KeySpec="AES_256")
        self.data_key = response["Plaintext"]  # plaintext key in bytes
        self.ciphertext_blob = response[
            "CiphertextBlob"
        ]  # opaque blob for storage/transport
        return self.data_key

    def encrypt_payload(self, plaintext: str) -> CiphertextPayload:
        """Encrypt plaintext using locally generated AES key derived from KMS data key."""
        if not self.data_key:
            raise RuntimeError(
                "Data key not initialized. Call generate_data_key first."
            )
        aes = AES.new(self.data_key, AES.MODE_GCM)
        ciphertext, tag = aes.encrypt_and_digest(plaintext.encode())
        # Combine nonce, ciphertext, tag for transport
        nonce = aes.nonce
        encrypted_blob = nonce + ciphertext + tag
        return CiphertextPayload(
            ciphertext=base64.b64encode(encrypted_blob).decode(),
            key_id=self.ciphertext_blob.hex(),  # store opaque blob identifier
        )

    def decrypt_payload(
        self, ciphertext_payload: CiphertextPayload
    ) -> PlaintextPayload:
        """Decrypt ciphertext using cached data key and KMS to unwrap data key."""
        if not self.data_key:
            raise RuntimeError(
                "Data key not initialized. Call generate_data_key first."
            )
        # Retrieve and unwrap KMS data key if needed for re-encryption scenarios
        # Here we simply reuse the cached data key for decryption
        aes = AES.new(
            self.data_key, AES.MODE_GCM, nonce=ciphertext_payload.ciphertext[:12]
        )
        ciphertext = ciphertext_payload.ciphertext[12:-16]
        tag = ciphertext_payload.ciphertext[-16:]
        plaintext = aes.decrypt_and_digest(ciphertext + tag)
        return PlaintextPayload(plaintext=plaintext.decode())


# Example usage
if __name__ == "__main__":
    # Load KMS key ID from environment
    KMS_KEY_ID = os.getenv("AWS_KMS_KEY_ID")
    if not KMS_KEY_ID:
        raise RuntimeError("Set AWS_KMS_KEY_ID environment variable before running.")
    encryptor = EnvelopeEncryptor(region_name="us-east-1")
    encryptor.generate_data_key(KMS_KEY_ID)
    plaintext = "Sensitive data that needs envelope encryption."
    ct_payload = encryptor.encrypt_payload(plaintext)
    print("Envelope encrypted payload (base64):", ct_payload.ciphertext)
    # Decryption (in practice you would unwrap the data key via KMS first for highest security)
    pt_payload = encryptor.decrypt_payload(ct_payload)
    print("Decrypted plaintext:", pt_payload.plaintext)
