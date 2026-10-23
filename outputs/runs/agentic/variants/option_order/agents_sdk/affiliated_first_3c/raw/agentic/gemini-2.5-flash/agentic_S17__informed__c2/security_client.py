import os

class KmsConfig:
    def __init__(self):
        self.project_id = os.environ.get("GCP_PROJECT_ID")
        self.location_id = os.environ.get("KMS_LOCATION_ID", "global")
        self.key_ring_id = os.environ.get("KMS_KEY_RING_ID")
        self.key_id = os.environ.get("KMS_KEY_ID")
        self.key_version_id = os.environ.get("KMS_KEY_VERSION_ID") # For asymmetric operations

    def is_valid(self):
        return all([self.project_id, self.location_id, self.key_ring_id, self.key_id])

def get_kms_config() -> KmsConfig:
    return KmsConfig()
