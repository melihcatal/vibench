# [HELPER] security_client.py

import os
from google.cloud import kms_v1

# Concrete Google Cloud KMS client using the official SDK.
class KmsClient:
    """Wrapper around google-cloud-kms that handles credentials and common operations."""
    def __init__(self):
        # The client picks up GOOGLE_APPLICATION_CREDENTIALS automatically.
        self.client = kms_v1.KeyManagementServiceClient()

    def encrypt(self, request: kms_v1.types.EncryptRequest):
        """Encrypt plaintext with a KMS CryptoKey."""
        return self.client.encrypt(request=request)

    def decrypt(self, request: kms_v1.types.DecryptRequest):
        """Decrypt ciphertext with a KMS CryptoKey."""
        return self.client.decrypt(request=request)

    def sign(self, request: kms_v1.types.SignRequest):
        """Sign data with an asymmetric KMS CryptoKey."""
        return self.client.sign(request=request)

    def verify(self, request: kms_v1.types.VerifyRequest):
        """Verify a signature using an asymmetric KMS CryptoKey."""
        return self.client.verify(request=request)

# Example usage (for testing via __main__)
if __name__ == "__main__":
    client = KmsClient()
    print("KMS client initialized (Google Cloud KMS)")
