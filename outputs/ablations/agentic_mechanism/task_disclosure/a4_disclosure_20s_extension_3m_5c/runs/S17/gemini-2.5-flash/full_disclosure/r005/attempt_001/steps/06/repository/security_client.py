from google.cloud import kms_v1

class SecurityClient:
    def __init__(self, project_id: str, location_id: str, key_ring_id: str, key_id: str):
        self.client = kms_v1.KeyManagementServiceClient()
        self.key_name = self.client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    def get_key_name(self) -> str:
        return self.key_name
