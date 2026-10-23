import os
from google.cloud import kms
from dataclasses import dataclass

@dataclass
class KMSConfig:
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
    location_id: str = os.getenv("GOOGLE_KMS_LOCATION", "global")
    key_ring_id: str = os.getenv("GOOGLE_KMS_KEY_RING", "your-key-ring")
    key_id: str = os.getenv("GOOGLE_KMS_KEY_ID", "your-key-id")
    signing_key_id: str = os.getenv("GOOGLE_KMS_SIGNING_KEY_ID", "your-signing-key-id")

def get_kms_client() -> kms.KeyManagementServiceClient:
    return kms.KeyManagementServiceClient()