import os
import boto3
from botocore.exceptions import ClientError

# Helper client for AWS services

class SecurityClient:
    """Local configuration and client helper utilities for Key Management and Encryption."""

    def __init__(self, key_id):
        # Use environment variable for credentials
        self.key_id = key_id
        self.kms_client = boto3.client('kms')

    def encrypt(self, plaintext):
        try:
            response = self.kms_client.encrypt(
                KeyId=self.key_id,
                Plaintext=plaintext
            )
            ciphertext_blob = response['CiphertextBlob']
            return ciphertext_blob
        except ClientError as e:
            raise RuntimeError(f"KMS encryption error: {e}")

    def decrypt(self, ciphertext_blob):
        try:
            response = self.kms_client.decrypt(
                CiphertextBlob=ciphertext_blob
            )
            plaintext = response['Plaintext'].decode('utf-8')
            return plaintext
        except ClientError as e:
            raise RuntimeError(f"KMS decryption error: {e}")

    def generate_data_key(self, key_spec='AES_256'):
        try:
            response = self.kms_client.generate_data_key(
                KeyId=self.key_id,
                KeySpec=key_spec
            )
            plaintext_key = response['Plaintext']
            ciphertext_blob = response['CiphertextBlob']
            return plaintext_key, ciphertext_blob
        except ClientError as e:
            raise RuntimeError(f"KMS data key generation error: {e}")
