import os
from google.cloud import kms_v1

class KmsClient:
    def __init__(self):
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.location_id = os.environ.get("GOOGLE_CLOUD_KMS_LOCATION")
        self.key_ring_id = os.environ.get("GOOGLE_CLOUD_KMS_KEY_RING")
        self.client = kms_v1.KeyManagementServiceClient()

    def get_key_path(self, key_id: str) -> str:
        return self.client.crypto_key_path(
            self.project_id, self.location_id, self.key_ring_id, key_id
        )
