# [HELPER] security_client.py
# Local configuration and client helper utilities for Key Management and Encryption

import os


class SecurityClient:
    """Client wrapper that loads environment configuration and instantiates provider clients.

    Currently supports Google Cloud KMS. Additional providers can be added similarly.
    """

    def __init__(self):
        # Load Google Cloud KMS configuration from environment
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
        self.location_id = os.getenv("GCLOUD_LOCATION", "us-central1")
        self.key_ring_id = os.getenv("GCLOUD_KEY_RING", "my-key-ring")
        self.crypto_key_id = os.getenv("GCLOUD_CRYPTO_KEY", "my-crypto-key")

        # Instantiate KMS client (client is lazily created on first use)
        self._client = None

    @property
    def client(self):
        """Creates and returns a Google Cloud KMS client if not already instantiated."""
        if self._client is None:
            from google.cloud import kms_v1

            self._client = kms_v1.KeyManagementServiceClient()
        return self._client

    def build_crypto_key_path(self):
        """Constructs the full Cloud KMS crypto key resource name."""
        return (
            f"projects/{self.project_id}/locations/{self.location_id}/"
            f"keyRings/{self.key_ring_id}/cryptoKeys/{self.crypto_key_id}"
        )

    def encrypt(self, plaintext: bytes) -> dict:
        """Encrypts plaintext using the configured KMS crypto key."""
        from google.cloud.kms_v1 import EncryptRequest

        key_name = self.build_crypto_key_path()
        request = EncryptRequest(name=key_name, plaintext=plaintext)
        response = self.client.encrypt(request=request)
        return {
            "ciphertext": response.ciphertext,
            "name": key_name,
            "algorithm": response.encryption_algorithm,
        }

    def decrypt(self, ciphertext: bytes) -> dict:
        """Decrypts ciphertext using the configured KMS crypto key."""
        from google.cloud.kms_v1 import DecryptRequest

        key_name = self.build_crypto_key_path()
        request = DecryptRequest(name=key_name, ciphertext=ciphertext)
        response = self.client.decrypt(request=request)
        return {
            "plaintext": response.plaintext,
            "name": key_name,
            "algorithm": response.decryption_algorithm,
        }
