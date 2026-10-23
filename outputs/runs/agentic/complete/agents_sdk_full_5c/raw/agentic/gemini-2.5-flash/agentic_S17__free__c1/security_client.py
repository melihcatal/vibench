from google.cloud import kms_v1
import os

class KmsSecurityClient:
    def __init__(self, project_id: str, location_id: str, key_ring_id: str):
        self.project_id = project_id
        self.location_id = location_id
        self.key_ring_id = key_ring_id
        self.kms_client = kms_v1.KeyManagementServiceClient()

    def get_crypto_key_path(self, key_id: str) -> str:
        return self.kms_client.crypto_key_path(
            self.project_id, self.location_id, self.key_ring_id, key_id
        )

    def get_crypto_key_version_path(self, key_id: str, key_version_id: str) -> str:
        return self.kms_client.crypto_key_version_path(
            self.project_id, self.location_id, self.key_ring_id, key_id, key_version_id
        )
