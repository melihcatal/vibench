from google.cloud import kms_v1
import os

class KmsClientHelper:
    """Helper class for Google Cloud KMS client initialization and common configurations."""

    def __init__(self):
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
        self.location = os.environ.get("GOOGLE_CLOUD_KMS_LOCATION", "global")
        self.key_ring = os.environ.get("GOOGLE_CLOUD_KMS_KEY_RING")
        self.key_name = os.environ.get("GOOGLE_CLOUD_KMS_KEY_NAME")
        self.key_version = os.environ.get("GOOGLE_CLOUD_KMS_KEY_VERSION")

        if not self.project_id or not self.key_ring or not self.key_name:
            raise ValueError("Missing Google Cloud KMS environment variables. Ensure GOOGLE_CLOUD_PROJECT_ID, GOOGLE_CLOUD_KMS_KEY_RING, and GOOGLE_CLOUD_KMS_KEY_NAME are set.")

        self.client = kms_v1.KeyManagementServiceClient()

    def get_client(self) -> kms_v1.KeyManagementServiceClient:
        return self.client

    def get_key_path(self, key_name: str = None, key_ring: str = None, location: str = None) -> str:
        return self.client.crypto_key_path(
            self.project_id,
            location or self.location,
            key_ring or self.key_ring,
            key_name or self.key_name,
        )

    def get_crypto_key_version_path(self, key_name: str = None, key_ring: str = None, location: str = None, key_version: str = None) -> str:
        return self.client.crypto_key_version_path(
            self.project_id,
            location or self.location,
            key_ring or self.key_ring,
            key_name or self.key_name,
            key_version or self.key_version
        )
